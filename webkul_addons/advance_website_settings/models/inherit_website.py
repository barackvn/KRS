# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import fields, models,api
from odoo import models
from odoo.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class website(models.Model):
	_inherit = 'website'

	redirect_to_cart =  fields.Selection([('same','Product Page'),('cart','Cart Summary'), ('previous_page','Same Page')], string='Redirect page after adding to cart',default='same')
	sub_total = fields.Boolean(string = 'Show Subtotal')
	minimum_order_value = fields.Float(string = 'Minimum Cart Value To Validate Order')
	c_id = fields.Many2one('res.currency', 'Cart Currency',default=lambda self: self.env.user.company_id.currency_id.id,required=True)


	def show_subTotal(self):
		ir_default = self.env['website'].sudo().get_current_website().sub_total
		return True if ir_default == None else ir_default
