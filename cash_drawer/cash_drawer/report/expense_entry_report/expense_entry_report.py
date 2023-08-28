# Copyright (c) 2013, Techstation and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _

def execute(filters=None):
        conditions, filters = get_conditions(filters)
        columns = get_column()
        data = get_data(conditions,filters)
        return columns,data

def get_column():
        return [_("Date") + ":Date:100",
				_("ID") + ":Link/Expense Entry:140",
                _("User") + ":Data:150",
				_("Expense Type") + ":Link/Expense Type:100",
                _("Mode of Payment") + ":Link/Mode of Payment:120",
				_("Supplier") + ":Data:100",
				_("Expense Amount") + ":Currency:150",
				_("Remarks") + ":Data:150",
				_("Reference No") + ":Data:150",
				_("Reference Date") + ":Date:150",
				_("Company") + ":Link/Company:140"]

def get_data(conditions,filters):
        invoice = frappe.db.sql("""SELECT
				posting_date,name,(select full_name from `tabUser` where name = drawer_user),expense_type,mode_of_payment,supplier_name,expense_amount,
				remarks,reference_no,reference_date,company
		FROM
    			`tabExpense Entry`
		WHERE
			docstatus = 1 %s 
			group by drawer_user,expense_type order by posting_date;"""%conditions, filters, as_list=1)
        return invoice

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"): conditions += " and posting_date >= %(from_date)s"
	if filters.get("to_date"): conditions += "and posting_date <= %(to_date)s"
	if filters.get("drawer_user"): conditions += " and drawer_user = %(drawer_user)s"
	if filters.get("expense_type"): conditions += " and expense_type = %(expense_type)s"
	if filters.get("company"): conditions += " and company = %(company)s"

	return conditions, filters