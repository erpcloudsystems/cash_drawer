# -*- coding: utf-8 -*-
# Copyright (c) 2020, Techstation and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from cash_drawer.cash_drawer.doctype.closing_controller import CommonClosing
from frappe.utils.data import flt


class SalesDrawer(CommonClosing):
	balance_type = "Seller"

	def validate(self):
		inc_cash_amount = 0.0
		inc_bank_amount = 0.0
		exp_cash_amount = 0.0
		exp_bank_amount = 0.0
		for p_type in self.transaction:
			if p_type.type == "Cash" and p_type.payment_type == "Receive":
				inc_cash_amount += p_type.paid_amount
			if p_type.type == "Cash" and p_type.payment_type == "Pay":
				exp_cash_amount += p_type.paid_amount	

			if p_type.type == "Bank" and p_type.payment_type == "Receive":
				inc_bank_amount += p_type.paid_amount
			if p_type.type == "Bank" and p_type.payment_type == "Pay":
				exp_bank_amount += p_type.paid_amount

		for p_type in self.pos_transaction:
			if p_type.type == "Cash" and p_type.payment_type == "Receive":
				inc_cash_amount += p_type.paid_amount
			if p_type.type == "Cash" and p_type.payment_type == "Pay":
				exp_cash_amount += p_type.paid_amount	

			if p_type.type == "Bank" and p_type.payment_type == "Receive":
				inc_bank_amount += p_type.paid_amount
			if p_type.type == "Bank" and p_type.payment_type == "Pay":
				exp_bank_amount += p_type.paid_amount			

		self.income_cash = inc_cash_amount
		self.income_bank = inc_bank_amount
		self.expense_cash = exp_cash_amount
		self.expense_bank = exp_bank_amount
		self.balance_cash = flt(inc_cash_amount - exp_cash_amount)
		self.balance_bank = flt(inc_bank_amount -exp_bank_amount)

	def on_submit(self):
		self.update_transactions()
		self.update_balance()

	def on_cancel(self):
		self.update_transactions()
		self.update_balance()

	def update_transactions(self):
		n = len(self.transaction)
		for d in self.transaction:
			sv = frappe.get_doc("Payment Entry", d.transaction_number)
			sv.added_in_cd = 1 if self.docstatus == 1 else 0
			sv.flags.ignore_validate_update_after_submit = True
			sv.save()
		frappe.msgprint(('Drawer Balance Updated'))

		for d in self.pos_transaction:
			sv = frappe.get_doc("Sales Invoice", d.transaction_number)
			sv.dc = 1 if self.docstatus == 1 else 0
			sv.flags.ignore_validate_update_after_submit = True
			sv.save()
		frappe.msgprint(('Drawer Balance Updated'))


@frappe.whitelist(allow_guest=True)
def insert_data(user, from_date=None, to_date=None):
	fields = ["pe.name as transaction_number"]
	filters = [
		"pe.docstatus = 1",
		"pm.create_payment_entry_on_delivery = 0",
		"pe.added_in_cd = 0",
		"pe.owner = '%s'" % user,
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
def insert_data_si(user, from_date=None, to_date=None):
	fields = [
		"`tabSales Invoice Payment`.mode_of_payment as mode_of_payment",
		"posting_date as date",
		"`tabSales Invoice`.name as transaction_number",
		"`tabSales Invoice Payment`.amount as paid_amount",
	]
	filters = [
		["Sales Invoice", "dc", "=", 0],
		["Sales Invoice", "is_pos", "=", 1],
		["Sales Invoice", "docstatus", "=", 1],
		["Sales Invoice", "owner", "=", user],
	]
	if from_date:
		filters.append(["Sales Invoice", "creation", ">=", from_date])
	if to_date:
		filters.append(["Sales Invoice", "creation", "<=", to_date])
	data = frappe.get_all(
		"Sales Invoice",
		filters,
		fields,
		update={"payment_type": "Receive"},
		group_by="`tabSales Invoice Payment`.name",
	)
	for d in data:
		if flt(d.paid_amount) < 0:
			d.payment_type = "Pay"
			d.paid_amount = abs(flt(d.paid_amount))
	return data

@frappe.whitelist(allow_guest=True)
def auto_close_sales_drawer():
	from datetime import datetime
	now = datetime.now()
	current_time = now.strftime("%H")
	
	for user in frappe.db.get_list("User",filters={'enabled':1},fields=['name']):
		print(current_time)
		if frappe.db.get_value('Cash Drawer User Table',{'type':"Sales Drawer",'user':user.name,'closing_time_croped':current_time},['name']):
			transaction = []
			pos_transaction = []
			for d in insert_data(user.name, from_date=None, to_date=None):
				transaction.append({'transaction_number':d.transaction_number,'date':d.date,'paid_amount':d.paid_amount,
				'mode_of_payment':d.mode_of_payment,'payment_type':d.payment_type})

			for d in insert_data_si(user.name, from_date=None, to_date=None):
				pos_transaction.append({'transaction_number':d.transaction_number,'date':d.date,'paid_amount':d.paid_amount,
				'mode_of_payment':d.mode_of_payment,'payment_type':d.payment_type})

			if len(transaction) > 0 or len(pos_transaction) > 0:
				scheduler = frappe.get_doc({
					"doctype": "Sales Drawer",
					"user": user.name,
					"auto_closed": "Yes",
					"transaction": transaction,
					"pos_transaction": pos_transaction,
				})
				scheduler.insert(ignore_permissions=True, ignore_mandatory=True)
				scheduler.save()
				scheduler.submit()