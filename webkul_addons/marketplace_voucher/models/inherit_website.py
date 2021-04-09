# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
from odoo import api, fields, models, _
from odoo import tools
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


class Website(models.Model):
	_inherit = 'website'

	@api.model
	def get_voucher_product_price(self, sale_order, voucher_obj, voucher_product_id):
		res = super(Website, self).get_voucher_product_price(sale_order, voucher_obj, voucher_product_id)
		if voucher_obj and voucher_obj.marketplace_seller_id:
			order_lines = sale_order.order_line.filtered(lambda l: l.product_id.marketplace_seller_id and
				l.product_id.marketplace_seller_id.id == voucher_obj.marketplace_seller_id.id and not l.is_delivery)
			if order_lines:
				order_total_price = sum(order_lines.mapped("price_subtotal"))
				res.update({'order_total_price':order_total_price})
		return res
