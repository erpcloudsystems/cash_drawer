# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "cash_drawer"
app_title = "Cash Drawer"
app_publisher = "Techstation"
app_description = "App for user financial transaction"
app_icon = "octicon octicon-inbox"
app_color = "#3498db"
app_email = "developers@techstation.com.eg"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/cash_drawer/css/cash_drawer.css"
# app_include_js = "/assets/cash_drawer/js/cash_drawer.js"

# include js, css files in header of web template
# web_include_css = "/assets/cash_drawer/css/cash_drawer.css"
# web_include_js = "/assets/cash_drawer/js/cash_drawer.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "cash_drawer.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "cash_drawer.install.before_install"
# after_install = "cash_drawer.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "cash_drawer.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
    "Drawer Balance": "cash_drawer.cash_drawer.doctype.drawer_transfer.drawer_transfer.get_permission_query_conditions",
}
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Invoice": {
		"before_insert": "cash_drawer.doc_events.sales_invoice.before_insert"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"cron": {
		"0/30 * * * *": [
			"cash_drawer.cash_drawer.doctype.shipping_company_drawer.shipping_company_drawer.auto_close_sc_drawer",
		],
        "0/40 * * * *": [
			"cash_drawer.cash_drawer.doctype.sales_drawer.sales_drawer.auto_close_sales_drawer",
		],
        "0/50 * * * *": [
			"cash_drawer.cash_drawer.doctype.delegate_drawer.delegate_drawer.auto_close_delegate_drawer",
		]
	},
}

fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Drawer Transmutation-workflow_state",
                    "Payment Entry-added_in_cd",
                    "Sales Invoice-dc",
                ],
            ]
        ],
    },
    {
        "doctype": "Role",
        "filters": [["name", "in", ["Drawer Manager", "Drawer User", "Drawer Reports"]]],
    },
    {"doctype": "Workflow", "filters": [["name", "in", ["Drawer Transfer"]]]},
    {"doctype": "Workflow State", "filters": [["name", "in", ["Draft"]]]},
]

# Testing
# -------

# before_tests = "cash_drawer.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "cash_drawer.event.get_events"
# }

after_migrate = "cash_drawer.utils.migrate.auto_insert_cron"