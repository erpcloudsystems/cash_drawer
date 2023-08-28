// Copyright (c) 2021, Techstation and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expense Type', {
	refresh: function(frm) {
		frm.set_query("account", "expense_type_account", function (doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['Account', 'account_type', '=', "Expense Account"],
					['Account', 'is_group', '=', 0],
					['Account', 'company', '=', d.company]
				]
			};
		});
		
		frm.set_query("cost_center", "expense_type_account", function (doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['Cost Center', 'is_group', '=', 0],
					['Cost Center', 'company', '=', d.company]
				]
			};
		});
	}
});
