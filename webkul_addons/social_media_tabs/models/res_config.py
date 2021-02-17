# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
import logging
from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo import SUPERUSER_ID
_logger = logging.getLogger(__name__)

class SocialTabConfigSettings(models.TransientModel):
	_name = 'social.tab.config.settings'
	_inherit = 'res.config.settings'

	website_id = fields.Many2one('website', string="website", required=True ,default=lambda self: self.env['website'].search([])[0])

	tab_ids = fields.Many2many(comodel_name="social.media.tabs", string='Social Tabs', readonly=False, related="website_id.tab_ids")
	tabs_position = fields.Selection([('left','Left'),('right','Right')], string='Tab Position', readonly=False, related="website_id.tabs_position")
	tab_event = fields.Selection([('hover','Mouse Hover'),('click','Mouse Click'),('fixed','Fixed')] ,required=True, readonly=False, related="website_id.tab_event")
	quote = fields.Char(string="Quote", readonly=False, related="website_id.quote")
	color = fields.Char(string="Background Color", readonly=False, related="website_id.color")

