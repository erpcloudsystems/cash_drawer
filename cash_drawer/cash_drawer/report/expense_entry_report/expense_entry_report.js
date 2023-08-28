// Copyright (c) 2016, Techstation and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Expense Entry Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_start(),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_end(),
		},
		{
			"fieldname": "drawer_user",
			"label": __("Drawer User"),
			"fieldtype": "Link",
			"options":"User"
		},
		{
			"fieldname": "expense_type",
			"label": __("Expense Type"),
			"fieldtype": "Link",
			"options":"Expense Type"
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options":"Company"
		},
	]
};
