// Copyright (c) 2022, Techstation and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cash Drawer User Table', {
	type: function(frm,cdt,cdn) {
		var d = locals[cdt][cdn];
		frappe.model.set_value(d.doctype,d.name,'closing_time_croped',d.closing_time.split(":")[0]);
	},
	closing_time: function(frm,cdt,cdn) {
		var d = locals[cdt][cdn];
		frappe.model.set_value(d.doctype,d.name,'closing_time_croped',d.closing_time.split(":")[0]);
	}
});
