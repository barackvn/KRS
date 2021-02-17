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

class MarketplaceMassUploadConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_allow_mass_upload = fields.Boolean(
        string= "Enable to allow mass upload of inventory and products",
        group= 'odoo_marketplace.marketplace_seller_group',
        implied_group= 'marketplace_mass_upload.group_marketplace_mass_upload',
    )

    def set_values(self):
        super(MarketplaceMassUploadConfigSettings, self).set_values()
        self.env['ir.default'].sudo().set('res.config.settings', 'group_allow_mass_upload', self.group_allow_mass_upload)
        return True

    @api.model
    def get_values(self, fields=None):
        res = super(MarketplaceMassUploadConfigSettings, self).get_values()
        group_allow_mass_upload = self.env['ir.default'].sudo().get(
            'res.config.settings', 'group_allow_mass_upload')
        res.update({
            'group_allow_mass_upload':group_allow_mass_upload,
        })
        return res