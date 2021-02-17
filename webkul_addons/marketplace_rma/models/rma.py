# -*- coding: utf-8 -*-
##########################################################################
# 2010-2017 Webkul.
#
# NOTICE OF LICENSE
#
# All right is reserved,
# Please go through this link for complete license : https://store.webkul.com/license.html
#
# DISCLAIMER
#
# Do not edit or add to this file if you wish to upgrade this module to newer
# versions in the future. If you wish to customize this module for your
# needs please refer to https://store.webkul.com/customisation-guidelines/ for more information.
#
# @Author        : Webkul Software Pvt. Ltd. (<support@webkul.com>)
# @Copyright (c) : 2010-2017 Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# @License       : https://store.webkul.com/license.html
#
##########################################################################

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class RmaRma(models.Model):
	_inherit = 'rma.rma'

	marketplace_seller_id = fields.Many2one(related='product_id.marketplace_seller_id', string='Marketplace Seller', store=True)
	refund_status = fields.Selection(selection=[('new', 'New'),('requested', 'Requested'),('rejected', 'Rejected'),('approved', 'Approved'),('done', 'Done')], string="Refund Status", default='new')

	def view_new_delivery_order(self):
		self.ensure_one()
		view_id = self.env.ref('odoo_marketplace.marketplace_picking_stock_modified_form_view').id
		return {
			'name': 'New Delivery Order',
			'view_type': 'form',
			'view_mode': 'form',
			'views': [(view_id, 'form')],
			'res_model': 'stock.picking',
			'view_id': view_id,
			'type': 'ir.actions.act_window',
			'res_id': self.new_do_picking_id.id,
		}

	def view_return_delivery_order(self):
		self.ensure_one()
		view_id = self.env.ref('odoo_marketplace.marketplace_picking_stock_modified_form_view').id
		return {
			'name': 'New Delivery Order',
			'view_type': 'form',
			'view_mode': 'form',
			'views': [(view_id, 'form')],
			'res_model': 'stock.picking',
			'view_id': view_id,
			'type': 'ir.actions.act_window',
			'res_id': self.picking_id.id,
		}

	def request_for_refund(self):
		for obj in self:
			if obj.product_received:
				obj.refund_status = 'requested'

	def _set_inv_created(self):
		for obj in self:
			if obj.refund_invoice_id:
				obj.inv_created = True
				if obj.refund_invoice_id.invoice_payment_state != 'paid':
					obj.refund_status = 'approved'
				else:
					obj.refund_status = 'done'
			else:
				obj.inv_created = False