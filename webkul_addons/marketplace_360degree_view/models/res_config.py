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

class Marketplace360degreeConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_allow_360degree_view = fields.Boolean(
        string= "Enable to allow 360 degree view for Products",
        group= 'odoo_marketplace.marketplace_seller_group',
        implied_group= 'marketplace_360degree_view.group_for_mp_360degree_view',
    )

    def set_values(self):
        super(Marketplace360degreeConfigSettings, self).set_values()
        self.env['ir.default'].sudo().set('res.config.settings', 'group_allow_360degree_view', self.group_allow_360degree_view)
        return True

    @api.model
    def get_values(self, fields=None):
        res = super(Marketplace360degreeConfigSettings, self).get_values()
        group_allow_360degree_view = self.env['ir.default'].sudo().get(
            'res.config.settings', 'group_allow_360degree_view')
        res.update({
            'group_allow_360degree_view':group_allow_360degree_view,
        })
        return res
