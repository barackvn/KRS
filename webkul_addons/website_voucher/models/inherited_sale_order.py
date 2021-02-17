#  -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class sale_order(models.Model):
	_inherit = "sale.order"

	wk_coupon_value= fields.Float(
		string="Coupon Value",

	)

	@api.model
	def _add_voucher(self, wk_order_total , voucher_dict, so_id=False):
		voucher_product_id = voucher_dict['product_id']
		voucher_value = voucher_dict['value']
		voucher_id = voucher_dict['coupon_id']
		voucher_name = voucher_dict['coupon_name']
		total_available = voucher_dict['total_available']
		voucher_val_type = voucher_dict['voucher_val_type']
		cutomer_type = voucher_dict['customer_type']
		total_prod_voucher_price = voucher_dict['total_prod_voucher_price']
		if not self.ids:
			order_id = so_id
		else:
			order_id = self.ids[0]
		order_obj = self.browse(order_id)
		result={}
		already_exists = self.env['sale.order.line'].sudo().search([('order_id', '=', order_id), ('product_id', '=', voucher_product_id)])
		voucher_obj = self.env['voucher.voucher'].sudo().browse(voucher_id)
		if already_exists:
			result['status'] = False
			result['message']	= _('You can use only one coupon per order.')
		else:
			values = self._website_product_id_change(order_id, voucher_product_id, qty=1)
			values['name'] = voucher_name
			if cutomer_type == 'general':
				if voucher_val_type == 'amount':
					if voucher_obj.applied_on == 'specific':
						if total_prod_voucher_price > voucher_value:
							values['price_unit'] = -voucher_value
						else:
							values['price_unit'] = -total_prod_voucher_price
					else:
						if wk_order_total < voucher_value:
							values['price_unit'] = -wk_order_total
						else:
							values['price_unit'] = -voucher_value
				else:
					if voucher_obj.applied_on == 'specific':
						values['price_unit'] = -(total_prod_voucher_price * voucher_value)/100
					else:
						values['price_unit'] = -(wk_order_total * voucher_value)/100
			else:
				if voucher_id:
					history_objs = self.env['voucher.history'].search([('voucher_id','=',voucher_id)])
					amount_left = 0
					if history_objs:
						for hist_obj in history_objs:
							if hist_obj.order_id:
								if hist_obj.order_id.id == order_id:
									continue
							amount_left += voucher_obj._get_amout_left_special_customer(hist_obj)
					if wk_order_total < amount_left:
						values['price_unit'] = - wk_order_total
					else:
						values['price_unit'] = -amount_left
			values['product_uom_qty'] = 1
			values['wk_voucher_id'] = voucher_id
			line_id = self.env['sale.order.line'].sudo().create(values)
			status = self.env['voucher.voucher'].sudo().redeem_voucher_create_histoy(voucher_name, voucher_id, values['price_unit'],order_id, line_id.id, 'ecommerce',order_obj.partner_id.id)
			result['status'] = status
		return result


class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	wk_voucher_id = fields.Many2one(
		comodel_name="voucher.voucher",
		string="Voucher"
	)

	def unlink(self):
		product_id = self.env['ir.default'].sudo().get('res.config.settings', 'wk_coupon_product_id')
		for line in self:
			if line.product_id.id == product_id:
				if line.wk_voucher_id:
					self.env['voucher.voucher'].sudo().return_voucher(line.wk_voucher_id.id, line.id)
		return super(SaleOrderLine, self).unlink()


	@api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
	def _compute_amount(self):
		res = super(SaleOrderLine, self)._compute_amount()
		for line in self:
			if line.product_id.id == self.env["website"].wk_get_default_product():
				line.order_id.write({
					'wk_coupon_value': -(line.price_unit)
				})
		return res
