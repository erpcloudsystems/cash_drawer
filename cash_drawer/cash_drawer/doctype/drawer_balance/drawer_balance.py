# -*- coding: utf-8 -*-
# Copyright (c) 2019, Techstation and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, get_url
from frappe.model.document import Document
from frappe import _


class DrawerBalance(Document):
	def update_adjustment(self, adjustments, save=False):
		if adjustments:
			if "Drawer Manager" not in frappe.get_roles():
				frappe.msgprint(_("Only Drawer Manager can be edit."))
			else:
				for row in adjustments:
					balance_row = self.get("balance_details", {"mode_of_payment": row.get("mode_of_payment")})
					if balance_row:
						balance_row[0].set("balance", row.get("balance"))
					else:
						frappe.msgprint(_("Payment Method {} not fund in Balance Details").format(row.get("mode_of_payment")))
		self.set("adjustments", [])
		if save:
			self.save()

	def delete_all_transactions(self):
		for field in ("balance_details", "drawer_transfer", "closing_transaction", "transfer_transaction", "adjustments"):
			self.set(field, [])
		self.save()

@frappe.whitelist()
def update_adjustment(doc):
	doc = frappe.parse_json(doc)
	d = frappe.get_doc(doc)
	d.update_adjustment(doc.adjustments, True)
	d.reload()
	return d

@frappe.whitelist()
def update_status(transfer_doc="", status=""):
	frappe.db.sql(
		"""update `tabTransfer Transaction` set status = '{}' where transaction_no='{}'""".format(
			status, transfer_doc
		)
	)

@frappe.whitelist()
def get_drawer_settings():
	drawer_closing = 1
	drawer_settings = frappe.get_single("Drawer Settings")
	closing_permission = frappe.db.sql(
		"""select count(name) from `tabDrawer Closing` where date(creation) = '{}' and owner = '{}'""".format(
			frappe.utils.today(), frappe.session.user
		)
	)

	if closing_permission[0][0] > drawer_settings.number_of_closing_per_day:
		drawer_closing = 0
	return {
		"transfer": drawer_settings.enable_drawer_balance_transfer,
		"closing_per_day": drawer_settings.number_of_closing_per_day,
		"drawer_close_permission": drawer_closing,
	}
