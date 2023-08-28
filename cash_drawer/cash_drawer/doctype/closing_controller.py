from frappe.model.document import Document
import frappe
from frappe.utils import today, flt


class CommonClosing(Document):
	user_field = "user"
	cash_field = "balance_cash"
	bank_field = "balance_bank"

	def update_balance(self):
		if self.user and frappe.db.exists("Drawer Balance", self.user):
			doc = frappe.get_doc("Drawer Balance", self.user)

		else:
			doc = frappe.new_doc("Drawer Balance")
			doc.update({"date": today(), "user": self.get(self.user_field)})

		tr_row = {"transaction_no": self.name}
		exsisting_row = doc.get("closing_transaction", tr_row)

		if self.docstatus == 1:
			if self.doctype == "Sales Drawer":
				tr_row.update({"created_date": today(), "submitted_by": frappe.session.user,"amount": (flt(self.balance_cash) + flt(self.balance_bank))})
			else:
				tr_row.update({"created_date": today(), "submitted_by": frappe.session.user,"amount": (flt(self.cash_on_delivery) + flt(self.bank_instalment))})	

			if exsisting_row:
				exsisting_row[0].update(tr_row)
			else:
				doc.append("closing_transaction", tr_row)

		elif self.docstatus == 2 and exsisting_row:
			doc.remove(exsisting_row[0])

		if self._action == "submit":
			for pm, amount in {
				"Cash": self.get(self.cash_field),
				"Bank": self.get(self.bank_field),
			}.items():
				row = doc.get("balance_details", {"mode_of_payment": pm})
				if row:
					row = row[0]
				else:
					row = doc.append("balance_details", {"mode_of_payment": pm})
				row.set("balance", flt(row.balance) + flt(amount))

		elif self._action == "cancel":
			for pm, amount in {
				"Cash": self.get(self.cash_field),
				"Bank": self.get(self.bank_field),
			}.items():
				row = doc.get("balance_details", {"mode_of_payment": pm})
				if row:
					row = row[0]
				else:
					row = doc.append("balance_details", {"mode_of_payment": pm})
				row.set("balance", flt(row.balance) - flt(amount))
		doc.save()