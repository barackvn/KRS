# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import models, fields

class website(models.Model):
    _inherit = 'website'

    wk_show_notes_input =  fields.Boolean(string='Enable Order Message Field')
    wk_show_desire_date = fields.Boolean(string='Enable Desire Date Field')
    maxium_delivery_date = fields.Integer(string="Maximum Number Of Days", help="Maximum number of days from current date after which user will be restricted.")
    minimum_delivery_date = fields.Integer(string="Minimum Number Of Days", help="Minimum number of days from current date before which user will be restricted.")

    def check_order_notes_setting(self, value=False):
        if value == 1:
            show_desire_date = self.wk_show_desire_date
            return show_desire_date
        if value == 2:
            show_notes_input = self.wk_show_notes_input
            return show_notes_input
        return False
