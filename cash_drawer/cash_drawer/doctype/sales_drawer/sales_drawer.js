// Copyright (c) 2020, Techstation and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Drawer', {
	refresh: frm =>{
		frm.set_df_property("user", "read_only", !frappe.user.has_role("Drawer Manager"))
		if (!frm.doc.user && frm.is_new()) {
			frm.set_value("user", frappe.boot.user.name)
		}
	},
	user: frm => {
		if (frm.doc.user) {
			frappe.call({
				"method": "cash_drawer.cash_drawer.doctype.delegate_drawer.delegate_drawer.getName",
				args: {
					user: frm.doc.user
				},
				callback: function (r) {
					frm.set_value("dba", r.message);
				}
			});
		}
	},
	get_data: frm => {
		for (const [key, value] of Object.entries({ "transaction": "insert_data", "pos_transaction": "insert_data_si" })) {
			frm.clear_table(key);
			frappe.call({
				"method": `cash_drawer.cash_drawer.doctype.sales_drawer.sales_drawer.${value}`,
				args: {
					user: frm.doc.user,
					from_date: frm.doc.from_date,
					to_date: frm.doc.to_date
				},
				callback: function (r) {
					if (!r.xhr) {
						r.message.forEach(row => {
							frm.add_child(key, row)
						})
					}
					frm.refresh_field(key);
					frm.events.calculate_totals(frm)
				}
			});
		}
		if (frm.doc.user && frm.doc.dba) {
			frappe.model.with_doc("Drawer Balance", frm.doc.dba, function () {
				cur_frm.clear_table("balance_details");
				var tabletransfer = frappe.model.get_doc("Drawer Balance", frm.doc.dba);
				$.each(tabletransfer.balance_details, function (index, row) {
					var d = frm.add_child("balance_details");
					d.name1 = row.name;
					d.mode_of_payment = row.mode_of_payment;
					d.balance = row.balance;
					cur_frm.refresh_field("balance_details");
				});
			});
		}
	},
	calculate_totals: frm => {
		let ct = 0.0
		let bt = 0.0
		let ec = 0.0
		let eb = 0.0
		let fields = ["transaction", "pos_transaction"]
		fields.forEach(field => {
			if (frm.doc[field]) {
				frm.doc[field].forEach(row => {
					if (row.payment_type === "Receive" && ["Cash", "Cash on Delivery"].includes(row.mode_of_payment)) {
						ct += flt(row.paid_amount)
					} else if (row.payment_type === "Receive") {
						bt += flt(row.paid_amount)
					}
					if (row.payment_type === "Pay" && ["Cash", "Cash on Delivery"].includes(row.mode_of_payment)) {
						ec += flt(row.paid_amount)
					} else if (row.payment_type === "Pay") {
						eb += flt(row.paid_amount)
					}
				})
			}
		})
		frm.set_value("income_cash", ct);
		frm.set_value("income_bank", bt);
		frm.set_value("expense_cash", ec);
		frm.set_value("expense_bank", eb);
		frm.set_value("balance_cash", ct-ec);
		frm.set_value("balance_bank", bt-eb);
		
	},
	customise: function (frm) {
		frm.set_df_property('from_date', 'reqd', frm.doc.customise)
		frm.set_df_property('to_date', 'reqd', frm.doc.customise)
	},
	validate: function (frm) {
		frm.trigger('calculate_totals');
	},
});
