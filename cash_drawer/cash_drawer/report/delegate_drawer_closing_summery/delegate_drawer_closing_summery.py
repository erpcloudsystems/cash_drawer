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
        _("Delegate") + ":Link/Delegate:150",
        _("ID") + ":Link/Delegate Drawer:150",
        _("Cash On Delivery") + ":Currency:150",
        _("Bank Instalment") + ":Currency:150",
    ]


def get_data(conditions, filters):
    orders = frappe.db.sql(
        """select date(creation), delegate, name, cash_on_delivery, bank_instalment
		 from `tabDelegate Drawer` where 
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
    if filters.get("delegate"):
        conditions += "and delegate = %(delegate)s"

    return conditions, filters
