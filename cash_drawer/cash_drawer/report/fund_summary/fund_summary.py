# Copyright (c) 2013, ahmad and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, erpnext
from frappe.utils import flt
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_data(filters):
    filters_data = [
        ["company", "=", filters.get("company")],
        ["posting_date", ">=", filters.get("from_date")],
        ["posting_date", "<=", filters.get("to_date")],
    ]
    if filters.get("party_type"):
        filters_data.append(["party_type", "=", filters.get("party_type")])

    if filters.get("party"):
        filters_data.append(["party", "=", filters.get("party")])

    if filters.get("mode_of_payment"):
        filters_data.append(["mode_of_payment", "=", filters.get("mode_of_payment")])

    if filters.get("owner"):
        filters_data.append(["owner", "=", filters.get("owner")])

    if filters.get("payment_type"):
        filters_data.append(["payment_type", "=", filters.get("payment_type")])

    all_payment_entry = frappe.get_all("Payment Entry", filters=filters_data, fields=["*"])
    return all_payment_entry


def get_columns():
    return [
        {
            "label": _("Name"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Payment Entry",
            "width": 120,
        },
        {
            "label": _("Payment Type"),
            "fieldname": "payment_type",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": _("Mode of Payment"),
            "fieldname": "mode_of_payment",
            "fieldtype": "Link",
            "options": "Mode of Payment",
            "width": 120,
        },
        {
            "label": _("Party Type"),
            "fieldname": "party_type",
            "fieldtype": "Link",
            "options": "Party Type",
            "width": 140,
        },
        {"label": _("Party"), "fieldname": "party", "fieldtype": "Data", "width": 140},
        {
            "label": _("Account Paid From"),
            "fieldname": "paid_from",
            "fieldtype": "Link",
            "options": "Account",
            "width": 140,
        },
        {
            "label": _("Account Paid To"),
            "fieldname": "paid_to",
            "fieldtype": "Link",
            "options": "Account",
            "width": 140,
        },
        {
            "label": _("Paid Amount"),
            "fieldname": "base_paid_amount",
            "fieldtype": "Currency",
            "options": "paid_from_account_currency",
            "width": 180,
        },
    ]
