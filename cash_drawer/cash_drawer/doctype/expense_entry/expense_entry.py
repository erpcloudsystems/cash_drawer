# Copyright (c) 2021, Techstation and contributors
# For license information, please see license.txt

import frappe
from erpnext.accounts.utils import get_account_currency, get_fiscal_year
from frappe import _, throw, msgprint
from frappe.utils import flt, today

from frappe.model.document import Document

class ExpenseEntry(Document):
	def validate(self):
		self.validate_user()
		self.validate_exp_amount()

	def validate_user(self):
		user_list = frappe.db.get_all('Cash Drawer User Table',filters={'company': self.company},fields=['user']) or []
		users = []
		for user in user_list:
			users.append(user.user)

		if self.drawer_user not in users:
			throw(_("User <b>{0}</b> is not allowed to post expense entry. Please contact Admin for the same.").format(self.drawer_user))

	def validate_exp_amount(self):
		if self.expense_amount <= 0:
			throw(_("Expense Amount can not be <b>0.0</b> or less then <b>0.0</b>"))		

	def on_submit(self):
		payment_mode = frappe.db.get_value("Mode of Payment",self.mode_of_payment,'type')
		balance = frappe.db.get_value("Drawer Balance Summary",
			{"parent": self.drawer_user, "mode_of_payment": payment_mode}, "balance") or 0.0

		if balance and flt(balance) >= flt(self.expense_amount):
			self.make_credit_entry()
			self.make_debit_entry()
			self.make_payment_dr_entry()
			self.make_payment_cr_entry()
			update_balance(self,payment_mode)
		else:
			throw(_("You can not complete this transaction as Available Drawer Balance is <b>{0}</b>").format(flt(balance)))

	def on_cancel(self):
		payment_mode = frappe.db.get_value("Mode of Payment",self.mode_of_payment,'type')
		self.revert_gl_entry()
		revert_balance(self,payment_mode)

	def make_credit_entry(self):
		fiscal_year = get_fiscal_year(self.posting_date, company=self.company, as_dict=True)
		if self.expense_amount > 0:
			gl_entry_cr = frappe.new_doc("GL Entry")
			gl_entry_cr.posting_date = self.posting_date
			gl_entry_cr.party = self.supplier
			gl_entry_cr.party_type = "Supplier"
			gl_entry_cr.voucher_type = self.doctype
			gl_entry_cr.voucher_no = self.name
			gl_entry_cr.against_voucher_type = self.doctype
			gl_entry_cr.against_voucher = self.name
			gl_entry_cr.cost_center = self.cost_center
			gl_entry_cr.account = self.party_account
			gl_entry_cr.against = self.expense_account
			gl_entry_cr.credit = self.expense_amount
			gl_entry_cr.credit_in_account_currency = self.expense_amount
			gl_entry_cr.remarks = self.remarks or "No Remarks"
			gl_entry_cr.is_opening = "No"
			gl_entry_cr.is_advance = "No"
			gl_entry_cr.company = self.company
			gl_entry_cr.fiscal_year = fiscal_year.name
			gl_entry_cr.flags.ignore_permissions = True
			gl_entry_cr.flags.ignore_mandatory = True
			gl_entry_cr.insert()
			gl_entry_cr.save()
			gl_entry_cr.submit()

	def make_debit_entry(self):
		fiscal_year = get_fiscal_year(self.posting_date, company=self.company, as_dict=True)
		if self.expense_amount > 0:
			gl_entry_dr = frappe.new_doc("GL Entry")
			gl_entry_dr.posting_date = self.posting_date
			gl_entry_dr.voucher_type = self.doctype
			gl_entry_dr.voucher_no = self.name
			gl_entry_dr.cost_center = self.cost_center
			gl_entry_dr.account = self.expense_account
			gl_entry_dr.against = self.supplier
			gl_entry_dr.debit = self.expense_amount
			gl_entry_dr.debit_in_account_currency = self.expense_amount
			gl_entry_dr.remarks = self.remarks or "No Remarks"
			gl_entry_dr.is_opening = "No"
			gl_entry_dr.is_advance = "No"
			gl_entry_dr.company = self.company
			gl_entry_dr.fiscal_year = fiscal_year.name
			gl_entry_dr.flags.ignore_permissions = True
			gl_entry_dr.flags.ignore_mandatory = True
			gl_entry_dr.insert()
			gl_entry_dr.save()
			gl_entry_dr.submit()

	def make_payment_dr_entry(self):
		fiscal_year = get_fiscal_year(self.posting_date, company=self.company, as_dict=True)
		if self.expense_amount > 0:
			gl_entry_cr = frappe.new_doc("GL Entry")
			gl_entry_cr.posting_date = self.posting_date
			gl_entry_cr.party = self.supplier
			gl_entry_cr.party_type = "Supplier"
			gl_entry_cr.voucher_type = self.doctype
			gl_entry_cr.voucher_no = self.name
			gl_entry_cr.against_voucher_type = self.doctype
			gl_entry_cr.against_voucher = self.name
			gl_entry_cr.cost_center = self.cost_center
			gl_entry_cr.account = self.party_account
			gl_entry_cr.against = self.payment_from
			gl_entry_cr.debit = self.expense_amount
			gl_entry_cr.debit_in_account_currency = self.expense_amount
			gl_entry_cr.remarks = "Amount {0} to {1} <br> Amount {0} against {2} {3}".format(self.expense_account,self.supplier,self.doctype,self.name)
			gl_entry_cr.is_opening = "No"
			gl_entry_cr.is_advance = "No"
			gl_entry_cr.company = self.company
			gl_entry_cr.fiscal_year = fiscal_year.name
			gl_entry_cr.flags.ignore_permissions = True
			gl_entry_cr.flags.ignore_mandatory = True
			gl_entry_cr.insert()
			gl_entry_cr.save()
			gl_entry_cr.submit()

	def make_payment_cr_entry(self):
		fiscal_year = get_fiscal_year(self.posting_date, company=self.company, as_dict=True)
		if self.expense_amount > 0:
			gl_entry_dr = frappe.new_doc("GL Entry")
			gl_entry_dr.posting_date = self.posting_date
			gl_entry_dr.voucher_type = self.doctype
			gl_entry_dr.voucher_no = self.name
			gl_entry_dr.cost_center = self.cost_center
			gl_entry_dr.account = self.payment_from
			gl_entry_dr.against = self.supplier
			gl_entry_dr.credit = self.expense_amount
			gl_entry_dr.credit_in_account_currency = self.expense_amount
			gl_entry_dr.remarks = "Amount {0} to {1} <br> Amount {0} against {2} {3}".format(self.expense_account,self.supplier,self.doctype,self.name)
			gl_entry_dr.is_opening = "No"
			gl_entry_dr.is_advance = "No"
			gl_entry_dr.company = self.company
			gl_entry_dr.fiscal_year = fiscal_year.name
			gl_entry_dr.flags.ignore_permissions = True
			gl_entry_dr.flags.ignore_mandatory = True
			gl_entry_dr.insert()
			gl_entry_dr.save()
			gl_entry_dr.submit()

	def revert_gl_entry(self):
		gl = frappe.get_list('GL Entry', filters={'voucher_no': self.name}, fields=['name'])
		for i in gl:
			gl_entry = frappe.get_doc("GL Entry",i)
			gl_entry.cancel()
			gl_entry.delete()
		

def update_balance(self,payment_mode):
	drawer_balance = frappe.get_doc('Drawer Balance Summary',{'mode_of_payment':payment_mode,'parent':self.drawer_user})
	drawer_balance.balance -= flt(self.expense_amount)
	drawer_balance.save(ignore_permissions = True)

def revert_balance(self,payment_mode):
	drawer_balance = frappe.get_doc('Drawer Balance Summary',{'mode_of_payment':payment_mode,'parent':self.drawer_user})
	drawer_balance.balance += flt(self.expense_amount)
	drawer_balance.save(ignore_permissions = True)	


@frappe.whitelist()
def getdefault_Supplier(expense_type):
	supplier = frappe.db.sql(
		"""select supplier,supplier_name from `tabExpense Type Supplier` where 
		parent = '{0}' and default_supplier = 1;""".format(expense_type),as_dict = True)

	return supplier[0] if supplier else False

@frappe.whitelist()
def get_drawer_balance(drawer_user,mode):
	payment_mode = frappe.db.get_value("Mode of Payment",mode,'type')
	balance = frappe.db.sql(
		"""select balance from `tabDrawer Balance Summary` where 
		parent = '{0}' and mode_of_payment = '{1}';""".format(drawer_user,payment_mode),as_dict = True)

	return balance[0] if balance else 0.0	