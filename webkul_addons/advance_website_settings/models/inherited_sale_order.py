# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models
from odoo.http import request
import logging
_log = logging.getLogger(__name__)
class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'


	def get_subtotal_cart(self, line):
		if line:
			self_obj = self.browse(line)
			price = self_obj.price_unit
			quantity = self_obj.product_uom_qty
			return price*quantity

	def get_subtotal_deleted(self, line):
		if line:
			
			price = line.product_id.lst_price
			quantity = line.product_uom_qty
			return price*quantity


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	def get_show_subtotal(self):

		
		ir_default = self.env['website'].sudo().get_current_website().sub_total
		return True if ir_default == None else ir_default
	def get_minimun_cart_value(self):
		
		ir_default = self.env['website'].get_current_website().c_id._convert(
                    self.env['website'].get_current_website().minimum_order_value, request.env['website'].get_current_website().pricelist_id.currency_id, self.env.user.company_id,
                    fields.Date.today()
                    )
		
		return 1 if ir_default == None else round(ir_default, 2)
	@api.model
	def _get_errors(self, order):
		
		minimum_order_value =1 if self.env['website'].sudo().get_current_website().minimum_order_value == None else self.env['website'].sudo().get_current_website().c_id._convert(
                    self.env['website'].sudo().get_current_website().minimum_order_value, self.env['website'].sudo().get_current_pricelist().currency_id, self.env.user.company_id,
                    fields.Date.today()
                    )
		minimum_order_value = round(minimum_order_value,2)
		errors = []
		if order and order.amount_total < minimum_order_value:
			errors.append(['Invalid Cart Value',"A minimum purchase total of %s%s is required to confirm your order, current purchase total is %s%s "%(order.currency_id.symbol ,minimum_order_value, order.currency_id.symbol ,order.amount_total)])
		return errors
