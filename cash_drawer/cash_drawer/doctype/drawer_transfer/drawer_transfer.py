# -*- coding: utf-8 -*-
# Copyright (c) 2019, Techstation and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _


class DrawerTransfer(Document):
    def validate(self):
        if frappe.db.exists(self.doctype, {"name": ("!=", self.name), "workflow_state": "Pending", "from_user": self.from_user}):
            frappe.throw(_("Already has a Pending Transfer Request"))
        
        if self.available_balance:
            if self.amount > self.available_balance:
                frappe.throw("Amount Is Higher Than Available Balance In Drawer")
        else:
            frappe.throw("Amount not available in drawer")
        
        if self.from_user == self.to_user:
            frappe.throw("From user and To user can not be same")

    def on_update_after_submit(self):
        frappe.msgprint(self.workflow_state)
        if self.workflow_state == "Reject":
            return False
        from_user_data = frappe.get_doc("Drawer Balance", self.from_user)
        for balance in from_user_data.balance_details:
            if balance.mode_of_payment == self.balance_type:
                balance.balance = balance.balance - self.amount
        row = from_user_data.append("transfer_transaction", {})
        row.created_date = self.creation
        row.recipient = self.to_user
        row.transaction_no = self.name
        row.submitted_by = frappe.session.user
        row.amount = -self.amount
        row.status = "Confirmed"
        row.mode_of_payment = self.balance_type
        from_user_data.flags.ignore_permissions=True
        from_user_data.save()

        drawer_balance = frappe.db.get_value("Drawer Balance", self.to_user, "name")
        if drawer_balance:
            doc = frappe.get_doc("Drawer Balance", self.to_user)
            found = False
            for balance in doc.balance_details:
                if balance.mode_of_payment == self.balance_type:
                    balance.balance = balance.balance + self.amount
                    found = True

            if found == False:
                row = doc.append("balance_details", {})
                row.mode_of_payment = self.balance_type
                row.balance = self.amount
        else:
            doc = frappe.new_doc("Drawer Balance")
            doc.date = self.creation
            doc.user = self.to_user
            row = doc.append("balance_details", {})
            row.mode_of_payment = self.balance_type
            row.balance = self.amount

        transfer_row = doc.append("transfer_transaction", {})
        transfer_row.created_date = self.creation
        transfer_row.transaction_no = self.name
        transfer_row.amount = self.amount
        transfer_row.recipient = self.from_user
        transfer_row.submitted_by = frappe.session.user
        transfer_row.status = "Confirmed"
        transfer_row.mode_of_payment = self.balance_type
        doc.flags.ignore_permissions=True
        doc.save()


def get_permission_query_conditions(user):
    if "Drawer Manager" in frappe.get_roles(user):
        return None
    if "Drawer User" in frappe.get_roles(user):
        return """(`tabDrawer Balance`.`name` = {user})""".format(user=frappe.db.escape(user))


@frappe.whitelist(allow_guest=True)
def getBalance(from_user, balance_type):
    balance = frappe.db.sql(
        """select dbs.balance from `tabDrawer Balance` db, `tabDrawer Balance Summary` dbs 
				where db.name = dbs.parent and db.user = '{0}' and dbs.mode_of_payment = '{1}';""".format(
            from_user, balance_type
        )
    )
    return balance[0][0] if balance else ""
