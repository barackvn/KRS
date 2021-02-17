# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
from odoo import api, fields, models, _


class WebkulWebsiteAddons(models.TransientModel):
    _inherit = 'webkul.website.addons'

    
    def get_stock_notify_configuration_view(self):
        ids = self.env['website.notifiy.config.settings'].search([])
        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('website_stock_notifiy.action_website_stock_notifiy')
        list_view_id = imd.xmlid_to_res_id('website_stock_notifiy.view_wk_website_stock_notify_tree')
        form_view_id = imd.xmlid_to_res_id('website_stock_notifiy.wk_website_stock_notify')

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[list_view_id, 'tree'], [form_view_id, 'form']],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
        }
        return result
