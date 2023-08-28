import frappe
from frappe import _, msgprint, throw
from frappe.utils import flt,get_link_to_form

@frappe.whitelist()
def getExp_Account(expense_type,company):
	expense_account = frappe.db.sql(
		"""select account,cost_center from `tabExpense Type Account` where 
		parent = '{0}' and company = '{1}' """.format(expense_type,company),as_dict = True)

	return expense_account[0] if expense_account else False	

@frappe.whitelist()
def get_bank_cash_account(mode_of_payment, company):
	account = frappe.db.get_value("Mode of Payment Account",
		{"parent": mode_of_payment, "company": company}, "default_account")

	return account if account else False