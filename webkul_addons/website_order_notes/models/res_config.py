# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import models, fields, api, _
from odoo.tools.translate import _
from odoo.exceptions import Warning

class WebsiteOrderNotesSettings(models.Model):
	_inherit = 'webkul.website.addons'
	_name = 'website.order.notes.settings'

	wk_show_notes_input =  fields.Boolean(string='Enable Order Message Field',related='website_id.wk_show_notes_input',readonly=False)
	wk_show_desire_date = fields.Boolean(string='Enable Desire Date Field',related='website_id.wk_show_desire_date',readonly=False)
	maxium_delivery_date = fields.Integer(string="Maximum Number Of Days", help="Maximum number of days from current date after which user will be restricted.",related='website_id.maxium_delivery_date',readonly=False)
	minimum_delivery_date = fields.Integer(string="Minimum Number Of Days", help="Minimum number of days from current date before which user will be restricted.",related='website_id.minimum_delivery_date',readonly=False)

	@api.constrains('maxium_delivery_date','minimum_delivery_date')
	def validation(self):
		if self.minimum_delivery_date>=self.maxium_delivery_date:
			raise Warning("Minimum number of days should be less than Maximum number of days.")
