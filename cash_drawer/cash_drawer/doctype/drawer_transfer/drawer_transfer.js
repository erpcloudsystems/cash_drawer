// Copyright (c) 2019, Techstation and contributors
// For license information, please see license.txt

frappe.ui.form.on('Drawer Transfer', {
	refresh: function (frm) {
		
		frm.set_df_property("from_user", "read_only", !frappe.user.has_role("Drawer Manager"))
		if (frm.is_new()) {
			if (!frappe.user.has_role("Drawer Manager")|| !frm.doc.from_user) {
				frm.set_value("from_user", frappe.session.user)
			}
		}
	}
});


frappe.ui.form.on('Drawer Transfer', {
	balance_type: function (frm) {
		if (frm.doc.balance_type) {
			frappe.call({
				"method": "cash_drawer.cash_drawer.doctype.drawer_transfer.drawer_transfer.getBalance",
				args: {
					from_user: frm.doc.from_user,
					balance_type: frm.doc.balance_type
				},
				callback: function (r) {
					console.log(r.message);
					frm.set_value("available_balance", r.message);
				}
			});
		}
	}
});


frappe.ui.form.on('Drawer Transfer', {
	validate: function (frm) {
		if (frappe.boot.user.name != frm.doc.from_user && !frappe.user.has_role("Drawer Manager")) {
			msgprint('From User Should Be Logged In User');
			validated = false;
		}
	}
});
