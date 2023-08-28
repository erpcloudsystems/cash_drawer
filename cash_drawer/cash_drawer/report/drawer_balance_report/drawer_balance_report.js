// Copyright (c) 2016, Techstation and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Drawer Balance Report"] = {
	"filters": [
		{
			"fieldname": "user",
			"label": __("User"),
			"fieldtype": "Link",
			"options":"User"
		},
		{
			"fieldname": "payment_mode",
			"label": __("Mode Of Payment"),
			"fieldtype": "Link",
			"options":"Mode of Payment"
		},
	]
}
