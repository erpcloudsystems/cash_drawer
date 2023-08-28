// Copyright (c) 2016, Techstation and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Seller Drawer Closing Summery"] = {
	"filters": [
		{
			"fieldname": "from_date",
	   		"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_start()
			},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_end()
		},
		{
			"fieldname": "user",
			"label": __("User"),
			"fieldtype": "Link",
			"options": "User",
		}
	]
};
