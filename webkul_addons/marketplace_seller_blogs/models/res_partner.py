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

from odoo import models,fields,api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    auto_blog_approve = fields.Boolean(string="Auto Blog Approve",
        default=lambda self: self.env['ir.default'].get('res.config.settings', 'mp_auto_blog_approve'), copy=False)

    @api.onchange("set_seller_wise_settings")
    def on_change_seller_wise_settings(self):
        if self.set_seller_wise_settings:
            res = super(ResPartner, self).on_change_seller_wise_settings()
            vals={}
            vals["auto_blog_approve"] = self.env['ir.default'].get(
                'res.config.settings', 'mp_auto_blog_approve')
            self.update(vals)
