# Copyright (c) 2013, Techstation and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	columns = [
		{
			"label": _("Mode of Payment"),
			"fieldname": "mode_of_payment",
			"fieldtype": "Link",
			"options": "Mode of Payment",
			"width": 120,
		},
		{   
			"label": _("User"), 
			"fieldname": "user",
			"fieldtype": "Data",
			"width": 140
		},
		{
			"label": _("Balance"),
			"fieldname": "balance",
			"fieldtype": "Currency",
			"width": 140
		},
		{
			"label": _("Last Closing Date"),
			"fieldname": "modified",
			"fieldtype": "Date",
			"width": 140,
		},
		{
			"label": _("Unclosed Amount"),
			"fieldname": "unclosed",
			"fieldtype": "Currency",
			"width": 140,
		},
	]
	condition = ""
	if filters.user and not filters.payment_mode:
		condition = "where tbs.name='{}'".format(filters.user)

	if not filters.user and filters.payment_mode:
		condition = "where tb.mode_of_payment='{}'".format(filters.payment_mode)

	if filters.user and filters.payment_mode:
		condition = "where tb.mode_of_payment='{}' and tbs.name='{}'".format(
			filters.payment_mode, filters.user
		)

	data = frappe.db.sql(
		"""select tb.mode_of_payment,tbs.name,tb.balance from `tabDrawer Balance Summary` tb inner join 
		`tabDrawer Balance` tbs on tbs.name = tb.parent {}""".format(condition)
	)
	balance_data = []
	for balance in data:
		balance_user = balance[1]
		balance_mode = balance[0]
		last_user_date = frappe.db.sql(
			"""select max(to_date) from `tabDrawer Closing` where user='{}'""".format(balance_user)
		)
		cash_drawer_pay = frappe.db.sql(
			"""select sum(paid_amount) as unclosed from `tabPayment Entry` pe where pe.owner = '{}' and 
			pe.mode_of_payment = '{}' and  NOT EXISTS (select * from `tabCash Drawer Reference` 
			cdr where cdr.document_no = pe.name) and pe.docstatus = 1 and pe.payment_type = 'Pay' """.format(
				balance_user, balance_mode
			)
		)
		invoice_data = frappe.db.sql(
			"""select sum(sip.amount) from `tabSales Invoice` si inner join 
			`tabSales Invoice Payment` sip on sip.parent = si.name where si.owner = '{}' 
			and si.docstatus = 1 and si.is_pos = 1 and sip.mode_of_payment = '{}' and
			NOT EXISTS(select * from `tabCash Drawer Reference` cdr where cdr.document_no = si.name)""".format(
				balance_user, balance_mode
			)
		)

		cash_drawer_recieve = frappe.db.sql(
			"""select sum(paid_amount) as unclosed from `tabPayment Entry` pe where pe.owner = '{}' and 
			pe.mode_of_payment = '{}' and NOT EXISTS (select * from `tabCash Drawer Reference` cdr where 
			cdr.document_no = pe.name) and pe.docstatus = 1 and pe.payment_type = 'Receive'""".format(
				balance_user, balance_mode
			)
		)
		unclosed = 0.00
		list_balance = [0.0]
		if last_user_date:
			if last_user_date[0][0] or "":
				balance_data.append(last_user_date[0][0])
				# list_balance.append(last_user_date[0][0])
		else:
			balance_data.append("2021-12-31")	

		if cash_drawer_recieve:
			pay = cash_drawer_recieve[0][0] or 0.00
			unclosed = unclosed + pay

		if invoice_data:
			rv = invoice_data[0][0] or 0.00
			unclosed = unclosed + rv

		if cash_drawer_pay:
			mv = cash_drawer_pay[0][0] or 0.00
			unclosed = unclosed - mv
		
		balance_data.append(unclosed)

	return columns, balance_data
