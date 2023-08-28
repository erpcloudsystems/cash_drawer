from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
        {
            "label": _("Master"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Sales Drawer",
                    "label": _("Sales Drawer"),
                    "description": _("Sales Drawer"),
                    "onboard": 1,
                },
            ]
        },                
        {
            "label": _("Delivery"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Delegate Drawer",
                    "label": ("Delegate Drawer"),
                    "description": _("Delegate Drawer"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Shipping Company Drawer",
                    "label": _("Shipping Company Drawer"),
                    "description": _("Shipping Company Drawer"),
                    "onboard": 1,
                },
            ],
        },
        {
            "label": _("Cash Drawer"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Payment Entry",
                    "label": _("Expense Entry"),
                    "description": _("Expense Entry"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Drawer Balance",
                    "label": _("Drawer Balance"),
                    "description": _("Drawer Balance"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Drawer Transfer",
                    "label": _("Drawer Transfer"),
                    "description": _("Drawer Transfer"),
                    "onboard": 1,
                },
            ],
        },
        {
            "label": _("Drawer Closing Reports"),
            "items": [
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Seller Drawer Closing Summery",
                    "label": _("Sales Drawer Summery"),
                    "doctype": "Seller Drawer Closing",
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Delegate Drawer Closing Summery",
                    "doctype": "Delegate Drawer Closing",
                    "label": _("Delegate Drawer Summary")
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Shipping Company Drawer Closing Summery",
                    "doctype": "Shipping Company Drawer Closing",
                    "label": _("Shipping Company Drawer Summary")
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Drawer Balance",
                    "doctype": "Drawer Balance",
                    "label": _("Drawer Balance Summery")
                },
            ],
        },
        {
            "label": _("Settings"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Drawer Settings",
                    "label": "Drawer Settings",
                    "description": _("Drawer Settings"),
                    "onboard": 1,
                }
            ],
        },
    ]
