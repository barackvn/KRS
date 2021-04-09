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

from odoo import models,fields,api,_

class MarketplaceConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mp_auto_blog_approve = fields.Boolean(string="Auto Blog Approve")

    def set_values(self):
        super(MarketplaceConfigSettings, self).set_values()
        self.env['ir.default'].sudo().set('res.config.settings', 'mp_auto_blog_approve', self.mp_auto_blog_approve)
        return True

    @api.model
    def get_values(self):
        res = super(MarketplaceConfigSettings, self).get_values()
        mp_auto_blog_approve = self.env['ir.default'].sudo().get('res.config.settings', 'mp_auto_blog_approve')
        res.update({
            'mp_auto_blog_approve':mp_auto_blog_approve,
        })
        return res
