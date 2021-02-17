# -*- coding: utf-8 -*-
#################################################################################
##    Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import SUPERUSER_ID
from odoo import http
from odoo.http import request
import datetime
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging
logger = logging.getLogger(__name__)


class WebsiteDailyDeals(WebsiteSale):
	def deal_update_cart(self):
		sale_order = request.website.sale_get_order()
		if sale_order:
			for line in sale_order.website_order_line:
				sale_order._cart_update(
					line_id=line.id,
					product_id=line.product_id.id,
					)

	@http.route(['/daily/deals'], type='http', auth="public", website=True)
	def website_daily_deals(self, **post):
		values={
			'daily_deals': request.env['website.deals'].sudo().get_valid_deals(),
			'page_header':request.env['website.deals'].sudo().get_page_header(),
			'pricelist':request.website.get_current_pricelist(),
			'datetime':datetime,
		}
		return http.request.render("website_daily_deals.daily_deals_page", values)

	@http.route(['/daily/deal/expired/<model("website.deals"):deal>'], type='json', auth="public", website=True)
	def website_deal_expired(self, deal,**post):
		if deal:
			deal.sudo().set_to_expired()
		return  deal and deal.state == 'expired'

	@http.route()
	def cart(self, **post):
		res = super(WebsiteDailyDeals,self).cart(**post)
		self.deal_update_cart()
		return res

	@http.route()
	def payment(self, **post):
		res = super(WebsiteDailyDeals,self).payment(**post)
		self.deal_update_cart()
		return res