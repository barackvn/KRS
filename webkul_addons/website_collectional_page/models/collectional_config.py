# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import models, fields, api, _

class WebsiteCollectionalConfig(models.TransientModel):
    _inherit="res.config.settings"

    collectional_page_label = fields.Char(string="Collection Page Link Label", default="Collection")
    show_collectional_menu = fields.Selection([('header','Show in header'),('footer','Show in footer'),('both', 'Show in header and footer')],
        string="Show Collection Menu", default="header")

    def set_values(self):
        super(WebsiteCollectionalConfig, self).set_values()
        self.env['ir.default'].sudo().set('res.config.settings', 'collectional_page_label', self.collectional_page_label)
        self.env['ir.default'].sudo().set('res.config.settings', 'show_collectional_menu', self.show_collectional_menu)
        return True

    @api.model
    def get_values(self):
        res = super(WebsiteCollectionalConfig, self).get_values()
        collectional_page_label = self.env['ir.default'].sudo().get('res.config.settings', 'collectional_page_label')
        show_collectional_menu = self.env['ir.default'].sudo().get('res.config.settings', 'show_collectional_menu')
        res.update({'collectional_page_label':collectional_page_label,
            'show_collectional_menu' : show_collectional_menu,
        })
        return res
