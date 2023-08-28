// Copyright (c) 2021, Techstation and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expense Entry', {
	refresh: function(frm) {
		frm.set_query("mode_of_payment", function () {
			return {
				query: "cash_drawer.utils.queries.get_mode_of_payment",
				filters: {
					'company': frm.doc.company
				}
			};
		});

		frm.set_query("expense_type", function () {
			return {
				query: "cash_drawer.utils.queries.get_expense_type",
				filters: {
					'company': frm.doc.company
				}
			};
		});

		frm.set_query("payment_from", function () {
			return {
				query: "cash_drawer.utils.queries.getAccount",
				filters: {
					'name': frm.doc.mode_of_payment,
					'company': frm.doc.company
				}
			};
		});

		frm.set_query("supplier", function () {
			return {
				query: "cash_drawer.utils.queries.getSupplier",
				filters: {
					'expense_type': frm.doc.expense_type,
				}
			};
		});

		frm.set_query("cost_center", function () {
			return {
				filters: {
					'company': frm.doc.company,
					'is_group': 0
				}
			};
		});

		if(frm.doc.docstatus == 0){
			frm.set_value('drawer_user',frappe.session.user);
		}

		if(frm.doc.docstatus > 0) {
			cur_frm.add_custom_button(__('Accounting Ledger'), function() {
				frappe.route_options = {
					voucher_no: frm.doc.name,
					from_date: frm.doc.posting_date,
					to_date: moment(frm.doc.modified).format('YYYY-MM-DD'),
					company: frm.doc.company,
					group_by: "Group by Voucher (Consolidated)",
					show_cancelled_entries: frm.doc.docstatus === 2
				};
				frappe.set_route("query-report", "General Ledger");
			}, __("View"));
		}
	},
	expense_type: function(frm) {
		set_supplier(frm);
		set_expense_account(frm);
		frm.set_value("expense_definition", "");
		frappe.call({
			method: "cash_drawer.utils.queries.get_exp_defination",
			args: {
				expense_type : frm.doc.expense_type
			},
			callback(r) {
				if (r.message) {
					if (r.message){
						const  values = []
						for (var val in r.message){
							console.log(r.message[val])
							values.push(r.message[val])
						}
						frm.set_df_property('expense_definition', 'options', [""].concat(values));

					}
				}
			}
		});
	},
	company: function(frm) {
		set_mode_of_payment(frm);
		set_expense_account(frm);
		set_party_account(frm);
	},
	mode_of_payment: function(frm) {
		set_mode_of_payment(frm);
		set_drawer_balance(frm);
	},
	supplier: function(frm) {
		set_party_account(frm);
	}
});

function set_mode_of_payment(frm) {
	if(frm.doc.mode_of_payment && frm.doc.company){
		frappe.call({
			"method": "cash_drawer.utils.account.get_bank_cash_account",
			args: {
				mode_of_payment: frm.doc.mode_of_payment,
				company: frm.doc.company
			},
			callback: function (r) {
				if(r.message){
					frm.set_value("payment_from", r.message);
				}
				else{
					frm.set_value("payment_from", "");
					frappe.throw(__("Please add Account in Mode of payment first."))
				}
			}
		});
	}
}

function set_expense_account(frm) {
	if(frm.doc.expense_type && frm.doc.company){
		frappe.call({
			"method": "cash_drawer.utils.account.getExp_Account",
			args: {
				company: frm.doc.company,
				expense_type: frm.doc.expense_type
			},
			callback: function (r) {
				if(r.message){
					frm.set_value("expense_account", r.message.account);
					frm.set_value("cost_center", r.message.cost_center);
				}
				else{
					frm.set_value("expense_account", "");
					frm.set_value("cost_center", "");
					frappe.throw(__("Please add Account & Cost Center in Expense Type first."))
				}	
			}
		});
	}
}

function set_supplier(frm) {
	if(frm.doc.expense_type && frm.doc.company){
		frappe.call({
			"method": "cash_drawer.cash_drawer.doctype.expense_entry.expense_entry.getdefault_Supplier",
			args: {
				expense_type: frm.doc.expense_type
			},
			callback: function (r) {
				if(r.message){
					frm.set_value("supplier", r.message.supplier);
					frm.set_value("supplier_name", r.message.supplier_name);
				}
				else{
					frm.set_value("supplier", "");
					frm.set_value("supplier_name", "");
					frappe.throw(__("Please add default supplier in expense type first."))
				}	
			}
		});
	}
}

function set_party_account(frm) {
	if(frm.doc.supplier && frm.doc.company && frm.doc.posting_date){
		frappe.call({
			"method": "erpnext.accounts.doctype.payment_entry.payment_entry.get_party_details",
			args: {
				company: frm.doc.company,
				party_type: "Supplier",
				party: frm.doc.supplier,
				date: frm.doc.posting_date
			},
			callback: function (r) {
				frm.set_value("party_account", r.message.party_account);
			}
		});
	}
}

function set_drawer_balance(frm) {
	if(frm.doc.drawer_user && frm.doc.mode_of_payment){
		frappe.call({
			"method": "cash_drawer.cash_drawer.doctype.expense_entry.expense_entry.get_drawer_balance",
			args: {
				drawer_user: frm.doc.drawer_user,
				mode: frm.doc.mode_of_payment
			},
			callback: function (r) {
				console.log(r.message);
				frm.set_value('drawer_balance',r.message.balance);
			}
		});
	}
}