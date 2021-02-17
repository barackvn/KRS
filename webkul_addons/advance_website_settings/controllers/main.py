# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import http
from odoo.http import request
from odoo import SUPERUSER_ID
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging
_logger = logging.getLogger(__name__)


class website_sale(WebsiteSale):
	def _filter_attributes(self, **kw):
		return {k: v for k, v in kw.items() if "attribute" in k}

	def get_redirect_url(self, product_id):
		url = "/shop/cart"
		redirect_to_cart = request.website.redirect_to_cart

		if redirect_to_cart == 'same' and product_id:
			product = request.env['product.product'].sudo().browse(int(product_id))
			if product:
				url = '/shop/product/%s' % slug(product.product_tmpl_id)
		elif redirect_to_cart == "previous_page":
			url = request.httprequest.referrer

		return url

	@http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
	def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
		super(website_sale, self).cart_update(product_id, add_qty=add_qty, set_qty=set_qty, **kw)

		url = self.get_redirect_url(product_id)
		return request.redirect(url)

	@http.route("/wk_get_redirect_val", type='json', auth="public",website=True)
	def wk_get_redirect_val(self, product_id):
		url = self.get_redirect_url(product_id)
		return url

	@http.route(["/website/wk_lang"], type='json', auth="public", methods=['POST'], website=True)
	def website_langauge(self, code=False, **kw):
		code = code or request.website.default_lang_id.code
		lang_id = request.env['res.lang'].search([('code','=',code.replace('-','_'))])
		return {
			'sep_format': lang_id.grouping,
			'decimal_point': lang_id.decimal_point,
			'thousands_sep': lang_id.thousands_sep
		}


	def checkout_redirection(self, order):
		minimum_order_value = 1 if not request.website.minimum_order_value else request.website.minimum_order_value
		if  minimum_order_value and order.amount_total < minimum_order_value:
			return request.redirect('/shop/cart')
		return super(website_sale, self).checkout_redirection(order)
