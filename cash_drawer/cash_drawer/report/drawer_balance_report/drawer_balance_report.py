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
        {"label": _("User"), "fieldname": "user", "fieldtype": "Data", "width": 140},
        {"label": _("Balance"), "fieldname": "balance", "fieldtype": "Currency", "width": 140},
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
        """select tb.mode_of_payment,tbs.name,tb.balance from `tabDrawer Balance Summary` tb inner join `tabDrawer Balance` tbs on tbs.name = tb.parent {}""".format(
            condition
        )
    )
    return columns, data
