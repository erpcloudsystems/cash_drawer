import frappe


@frappe.whitelist()
def getAccount(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql(
		"""select default_account from `tabMode of Payment Account` where 
		parent = '{0}' and company = '{1}' """.format(filters.get("name"),filters.get("company"))
	)

@frappe.whitelist()
def getSupplier(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql(
		"""select supplier from `tabExpense Type Supplier` where 
		parent = '{0}'""".format(filters.get("expense_type"))
	)

# Setting Queries

@frappe.whitelist()
def get_mode_of_payment(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql(
		"""select mode_of_payment from `tabCash Drawer User Payment` where 
		company = '{0}'""".format(filters.get("company"))
	)

@frappe.whitelist()
def get_expense_type(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql(
		"""select expense_type from `tabCash Drawer User Expense` where 
		company = '{0}'""".format(filters.get("company"))
	)	

@frappe.whitelist()
def get_exp_defination(expense_type):
	return frappe.db.sql(
		"""select expense_definition from `tabExpense Definition` where 
		parent = '{0}'""".format(expense_type),as_list=True)