# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import models, fields, api, _

class account_invoice(models.Model):
	_inherit = "account.move"

	wk_invoice_notes = fields.Text('Notes',compute="_compute_order_notes")

	def _compute_order_notes(self):
		for invoice in self:
			order = self.env['sale.order'].sudo().search([('name','=',invoice.invoice_origin)], limit=1)
			self.wk_invoice_notes = order.wk_notes
