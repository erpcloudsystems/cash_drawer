# -*- coding: utf-8 -*-
# Copyright (c) 2020, Techstation and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from cash_drawer.cash_drawer.doctype.closing_controller import CommonClosing


class DelegateDrawer(CommonClosing):
	cash_field = "cash_on_delivery"
	bank_field = "bank_instalment"

	def validate(self):
		cash_amount = 0.0
		bank_amount = 0.0
		for p_type in self.transaction:
			if p_type.type == "Cash":
				cash_amount += p_type.paid_amount

			if p_type.type == "Bank":
				bank_amount += p_type.paid_amount

		self.cash_on_delivery = cash_amount
		self.bank_instalment = bank_amount

	def on_submit(self):
		self.update_balance()
		self.notify_update()

	def on_cancel(self):
		self.update_balance()
		self.notify_update()

	def notify_update(self):
		n = len(self.transaction)
		for d in self.transaction:
			sv = frappe.get_doc("Payment Entry", d.transaction_number)
			sv.added_in_cd = 1 if self.docstatus == 1 else 0
			sv.flags.ignore_validate_update_after_submit = True
			sv.save()
		frappe.msgprint(('Drawer Balance Updated'))


@frappe.whitelist(allow_guest=True)
def insert_data(delegate, from_date=None, to_date=None):
	fields = ["pe.name as transaction_number"]
	filters = [
		"pe.docstatus = 1",
		"pm.payment_recipient = 1",
		"pm.create_payment_entry_on_delivery = 1",
		"pe.shipping_by = 'Delegate'",
		"pe.shipping_source= '%s'" % delegate,
		"pe.added_in_cd = 0",
		"pe.payment_by_delivery_app = 1"
	]
	join = ""
	fields.extend(["pe.posting_date as date", "pe.paid_amount as paid_amount", "pe.mode_of_payment as mode_of_payment","pe.payment_type as payment_type"])
	if from_date:
		filters.append("date(pe.%s)>= date(%s)" % ("date" if error else "posting_date", from_date))
	if to_date:
		filters.append("date(pe.%s)<=date(%s)" % ("date" if error else "posting_date", to_date))
	return frappe.db.sql(
		"""select {fields} from `tabPayment Entry` pe{join} right join `tabMode of Payment` pm on pe.mode_of_payment=pm.name
		where {con}""".format(
			join = join,
			fields = ", ".join(fields),
			con = " and ".join(filters),
		),
		as_dict=True,
	)

@frappe.whitelist(allow_guest=True)
def getName(user):
	return frappe.get_value("Drawer Balance", {"user": user})

@frappe.whitelist(allow_guest=True)
def auto_close_delegate_drawer():
	from datetime import datetime
	now = datetime.now()
	current_time = now.strftime("%H")

	for user in frappe.db.get_list("User",filters={'enabled':1},fields=['name']):
		if frappe.db.get_value('Cash Drawer User Table',{'type':"Delegate Drawer",'user':user.name,'closing_time_croped':current_time},['name']):
			delegate = frappe.db.get_value('Delegate',{'user':user.name},['name'])
			transaction = []
			for d in insert_data(delegate, from_date=None, to_date=None):
				transaction.append({'transaction_number':d.transaction_number,'date':d.date,'paid_amount':d.paid_amount,
				'mode_of_payment':d.mode_of_payment,'payment_type':d.payment_type})
			if len(transaction) > 0:
				scheduler = frappe.get_doc({
					"doctype": "Delegate Drawer",
					"delegate": delegate,
					"auto_closed": "Yes",
					"transaction": transaction
				})
				scheduler.insert(ignore_permissions=True, ignore_mandatory=True)
				scheduler.save()
				scheduler.submit()