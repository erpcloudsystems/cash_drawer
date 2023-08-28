# Copyright (c) 2013, Techstation and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _


def execute(filters=None):
    conditions, filters = get_conditions(filters)
    columns = get_column()
    data = get_data(conditions, filters)
    return columns, data


def get_column():
    return [
        _("Date") + ":Date:120",
        _("User") + ":Link/User:150",
        _("ID") + ":Link/Sales Drawer:150",
        _("Income Cash") + ":Currency:150",
        _("Expense Cash") + ":Currency:150",
        _("Balance Cash") + ":Currency:150",
        _("Income Bank") + ":Currency:150",
        _("Expense Bank") + ":Currency:150",
        _("Balance Bank") + ":Currency:150",
    ]


def get_data(conditions, filters):
    orders = frappe.db.sql(
        """select DATE(creation), user, name, income_cash, expense_cash, balance_cash, income_bank, expense_bank, balance_bank
		 from `tabSales Drawer` where 
		docstatus = 1 %s order by creation asc;"""
        % conditions,
        filters,
        as_list=1,
    )
    return orders


def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " and creation >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and creation <= %(to_date)s"
    if filters.get("user"):
        conditions += "and user = %(user)s"

    return conditions, filters
