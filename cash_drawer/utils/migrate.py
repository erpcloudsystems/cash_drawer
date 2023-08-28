import frappe

def auto_insert_cron():
	if not frappe.db.exists('Scheduled Job Type', 'shipping_company_drawer.auto_close_sc_drawer'):
		scheduler = frappe.get_doc({
			"doctype": "Scheduled Job Type",
			"method": 'cash_drawer.cash_drawer.doctype.shipping_company_drawer.shipping_company_drawer.auto_close_sc_drawer',
			"frequency": 'Cron',
			"cron_format": "0/30 * * * *"
		})
		scheduler.insert(ignore_permissions=True, ignore_mandatory=True)
		scheduler.save()

	if not frappe.db.exists('Scheduled Job Type', 'sales_drawer.auto_close_sales_drawer'):
		scheduler = frappe.get_doc({
			"doctype": "Scheduled Job Type",
			"method": 'cash_drawer.cash_drawer.doctype.sales_drawer.sales_drawer.auto_close_sales_drawer',
			"frequency": 'Cron',
			"cron_format": "0/40 * * * *"
		})
		scheduler.insert(ignore_permissions=True, ignore_mandatory=True)
		scheduler.save()

	if not frappe.db.exists('Scheduled Job Type', 'delegate_drawer.auto_close_delegate_drawer'):
		scheduler = frappe.get_doc({
			"doctype": "Scheduled Job Type",
			"method": 'cash_drawer.cash_drawer.doctype.delegate_drawer.delegate_drawer.auto_close_delegate_drawer',
			"frequency": 'Cron',
			"cron_format": "0/50 * * * *"
		})
		scheduler.insert(ignore_permissions=True, ignore_mandatory=True)
		scheduler.save()		