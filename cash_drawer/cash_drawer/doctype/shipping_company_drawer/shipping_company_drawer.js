// Copyright (c) 2020, Techstation and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shipping Company Drawer', {
    shipping_company: function (frm) {
        if (frm.doc.shipping_company) {
            frappe.call({
                "method": "cash_drawer.cash_drawer.doctype.shipping_company_drawer.shipping_company_drawer.getName",
                args: {
                    doctype: "Shipping Company Drawer",
                    user: frm.doc.user
                },
                callback: function (r) {
                    frm.set_value("dba", r.message);
                }
            });
        }
    },
    get_data: frm => {
        for (const [key, value] of Object.entries({ "transaction": "insert_data"})) {
            frm.clear_table(key);
            frm.refresh_field(key);

            frappe.call({
                "method": `cash_drawer.cash_drawer.doctype.shipping_company_drawer.shipping_company_drawer.${value}`,
                args: {
                    shipping_company: frm.doc.shipping_company,
                    from_date: frm.doc.from_date,
                    to_date: frm.doc.to_date
                },
                callback: function (r) {
                    if (!r.xhr && r.message) {
                        r.message.forEach(row => {
                            frm.add_child(key, row);
                        })
                        frm.refresh_field(key)
                        if (key === "transaction") {
                            frm.events.calculate_mop_totals(frm)
                        }
                    }
                    if (r.message.length == 0) {
                        frappe.msgprint(__("No Pending Transaction Found For Shipping Company"));
                    }
                }
            });
        }
        if (frm.doc.delegate && frm.doc.dba) {
            frappe.model.with_doc("Drawer Balance", frm.doc.dba, function () {
                cur_frm.clear_table("balance_details");
                var tabletransfer = frappe.model.get_doc("Drawer Balance", frm.doc.dba);
                $.each(tabletransfer.balance_details, function (index, row) {
                    var d = frm.add_child("balance_details");
                    d.name1 = row.name;
                    d.mode_of_payment = row.mode_of_payment;
                    d.balance = row.balance;
                    cur_frm.refresh_field("balance_details");
                    //              frm.set_value("cb_value",frm.doc.closing_balance / a.length);
                });
            });
        }
    },
    calculate_mop_totals: frm => {
        if (frm.doc.transaction) {
            let total = 0.0
            let bt = 0.0
            frm.doc.transaction.forEach(row => {
                if (row.mode_of_payment == "Cash On Delivery") {
                    total += flt(row.paid_amount)
                }
                else {
                    bt += flt(row.paid_amount)
                }
            })
            frm.set_value("cash_on_delivery", total);
            frm.set_value("bank_instalment", bt);
        }
    },
    customise: function (frm) {
        frm.set_df_property('from_date', 'reqd', frm.doc.customise)
        frm.set_df_property('to_date', 'reqd', frm.doc.customise)
    }
});


frappe.ui.form.on('Shipping Company Drawer', "get_data", function (frm) {
    if (frm.doc.shipping_company && frm.doc.dba) {
        frappe.model.with_doc("Drawer Balance", frm.doc.dba, function () {
            cur_frm.clear_table("balance_details");
            var tabletransfer = frappe.model.get_doc("Drawer Balance", frm.doc.dba);
            $.each(tabletransfer.balance_details, function (index, row) {
                var d = frm.add_child("balance_details");
                d.name1 = row.name;
                d.mode_of_payment = row.mode_of_payment;
                d.balance = row.balance;
                cur_frm.refresh_field("balance_details");
                //              frm.set_value("cb_value",frm.doc.closing_balance / a.length);
            });
        });
    }
});
