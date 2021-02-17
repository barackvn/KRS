# -*- coding: utf-8 -*-
#################################################################################
##    Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################
from odoo import api, fields, models
from odoo.exceptions import UserError

class WebsiteDailyDealsConfig(models.TransientModel):
	_inherit = 'res.config.settings'
	_name = 'website.daily.deals.conf'
	_description = "website daily deals conf"

	@api.model
	def _get_deals_pricelist(self):
		xid = self.env['ir.model.data'].search([('module', '=', 'website_daily_deals'), ('name', '=', 'wk_deals_pricelist')])
		pricelist = 0
		if xid:
			pricelist = xid.res_id
		return pricelist

	show_page_header = fields.Boolean('Show Page Header', help="show Page header in website.")
	page_header_text = fields.Char('Page Header Text', default="DONT MISS A DEAL THIS TIME", help="Text for the header of the page to be displayed in website")
	item_to_show = fields.Selection([('banner_only','Banner Only'),('products_only','Products Only'), ('both','Both')],'What to Display on Website', default='both', help="choose what you want to display in website.")
	display_products_as = fields.Selection([('grid','Grid'),('slider','Slider')],'How to display Products on Website', default='grid', help="choose how to display the produts in website.")
	deal_pricelist = fields.Many2one('product.pricelist','Pricelist', required=True , help="Choose a pricelist, all the deal products will be added in that pricelist.(A default Deal pricelist will be created.)")
	show_message_before_expiry = fields.Boolean('Show Message before Expiry',help="Do you want to show a message before the expiry date of the deal, if yes then set this true.")
	message_before_expiry = fields.Char('Message before Expiry', help="The message you want to show in the website when deal is about to expire.")
	interval_before = fields.Integer('Time interval before to display message' , help="How much time before the expiry date you want to display the message.")
	unit_of_time = fields.Selection([('minutes','Minutes'),('hours','Hours'),('days','Days'),('weeks','Weeks'),('months','Months')],'Time Unit', default='hours')
	show_message_after_expiry = fields.Boolean('Show Message After Expiry', help="Do you want to show the message after the expiry date of the deal.")
	message_after_expiry = fields.Char('Message After Expiry', help="The message you want to show in the website when deal is expired.")
	d_state_after_expire = fields.Selection([('blur','Blur'),('delete','Delete')],'What to do with deal after Expiry', default='blur', help="What do you want to do with deal after expiration.Either you can blur the deals in website or delete a deal from website")

	@api.model
	def set_values(self):
		super(WebsiteDailyDealsConfig, self).set_values()
		IrDefault = self.env['ir.default'].sudo()
		IrDefault.set('website.daily.deals.conf', 'show_page_header',self.show_page_header)
		IrDefault.set('website.daily.deals.conf', 'page_header_text',self.page_header_text)
		IrDefault.set('website.daily.deals.conf', 'item_to_show',self.item_to_show)
		IrDefault.set('website.daily.deals.conf', 'display_products_as',self.display_products_as)
		IrDefault.set('website.daily.deals.conf', 'deal_pricelist',self.deal_pricelist.id)
		IrDefault.set('website.daily.deals.conf', 'show_message_before_expiry',self.show_message_before_expiry)
		IrDefault.set('website.daily.deals.conf', 'message_before_expiry',self.message_before_expiry)
		IrDefault.set('website.daily.deals.conf', 'interval_before',self.interval_before)
		IrDefault.set('website.daily.deals.conf', 'unit_of_time',self.unit_of_time)
		IrDefault.set('website.daily.deals.conf', 'show_message_after_expiry',self.show_message_after_expiry)
		IrDefault.set('website.daily.deals.conf', 'message_after_expiry',self.message_after_expiry)
		IrDefault.set('website.daily.deals.conf', 'd_state_after_expire',self.d_state_after_expire)
		return True


	@api.model
	def get_values(self):
		res = super(WebsiteDailyDealsConfig, self).get_values()
		IrDefault = self.env['ir.default'].sudo()
		res.update({
				'show_page_header':IrDefault.get('website.daily.deals.conf', 'show_page_header'),
				'page_header_text':IrDefault.get('website.daily.deals.conf', 'page_header_text'),
				'item_to_show':IrDefault.get('website.daily.deals.conf', 'item_to_show') or 'both',
				'display_products_as':IrDefault.get('website.daily.deals.conf', 'display_products_as') or 'grid',
				'message_before_expiry':IrDefault.get('website.daily.deals.conf', 'message_before_expiry'),
				'show_message_before_expiry':IrDefault.get('website.daily.deals.conf', 'show_message_before_expiry'),
				'interval_before':IrDefault.get('website.daily.deals.conf', 'interval_before'),
				'deal_pricelist':IrDefault.get('website.daily.deals.conf', 'deal_pricelist') or self._get_deals_pricelist(),
				'unit_of_time':IrDefault.get('website.daily.deals.conf', 'unit_of_time'),
				'show_message_after_expiry':IrDefault.get('website.daily.deals.conf', 'show_message_after_expiry'),
				'message_after_expiry':IrDefault.get('website.daily.deals.conf', 'message_after_expiry'),
				'd_state_after_expire':IrDefault.get('website.daily.deals.conf', 'd_state_after_expire'),
				})
		return res
