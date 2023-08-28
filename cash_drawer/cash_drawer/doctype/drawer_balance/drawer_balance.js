
// Copyright (c) 2019, Techstation and contributors
// For license information, please see license.txt

frappe.ui.form.on('Drawer Balance', {
	refresh: function (frm) {
		frm.disable_save()
		let options =[]
		frm.doc.balance_details.forEach(row=>{
			options.push(row.mode_of_payment)
		})
		frappe.meta.get_docfield("Cash Drawer Balance Adjustment", "mode_of_payment", frm.doc.name).options = options
		frm.fields_dict.adjustments.grid.refresh();

	},
	balances_adjustment: function(frm) {
		frappe.call({
			method: "cash_drawer.cash_drawer.doctype.drawer_balance.drawer_balance.update_adjustment",
			args: {
				doc: frm.doc
			},
			freeze: true,
			callback: r=>{
				if (!r.xhr) {
					frm.reload_doc()
				}
			}
		})
		
	}
});

frappe.ui.form.on('Transfer Transaction', {
	status: function (frm, cdt, cdn) {
		var d = locals[cdt][cdn]
		if (d.status == "Confirmed") {

			frappe.call({
				method: 'cash_drawer.cash_drawer.doctype.drawer_balance.drawer_balance.update_status',
				args: {
					transfer_doc: d.status,
				},
				callback: function (r) {
					frm.reload_doc();
				}
			});

		}
	}
});


frappe.ui.form.on('Cash Drawer Balance Adjustment', {
	mode_of_payment: function (frm, cdt, cdn) {
		let d = locals[cdt][cdn]
		if (d.mode_of_payment) {
			let total =0.0
			cur_frm.doc.balance_details.forEach(row => {
				if (row.mode_of_payment===d.mode_of_payment)
					total = flt(row.balance)
			});
			d.balance_before_adjustment = total
			cur_frm.refresh_field(d.parentfield)
		}
	}
});

