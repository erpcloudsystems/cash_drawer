# Copyright (c) 2021, Techstation and contributors
# For license information, please see license.txt

import frappe
from frappe import _, throw, msgprint
from frappe.model.document import Document

class ExpenseType(Document):
	def validate(self):
		self.validate_default_supplier()

	def validate_default_supplier(self):
		"""Error when No Default Supplier Found"""
		no_default_supplier = []
		for entry in self.supplier:
			if entry.default_supplier == 1:
				no_default_supplier.append(entry.supplier)
			if len(no_default_supplier) == 0:
				throw(_("No default supplier found. Please select 1 default supplier."))

			if len(no_default_supplier) > 1:
				throw(_("Only 1 supplier can be set as default."))				

		"""Error when Same Supplier selected More than once"""
		supplier_list = []
		for entry in self.supplier:
			supplier_list.append(entry.supplier)
			if len(supplier_list) != len(set(supplier_list)):
				throw(_("Same supplier added more then once."))