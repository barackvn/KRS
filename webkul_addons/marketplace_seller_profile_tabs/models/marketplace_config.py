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

class MarketplaceConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_seller_profile_tabs = fields.Boolean(
        group='odoo_marketplace.marketplace_seller_group',
        implied_group='marketplace_seller_profile_tabs.mp_seller_profile_tab_group',
        string="Allow seller for custom profile Tabs.",
        help="Allow seller to create additional profile tabs to display extra on website."
    )

    def set_values(self):
        super(MarketplaceConfigSettings, self).set_values()
        self.env['ir.default'].sudo().set('res.config.settings', 'group_seller_profile_tabs', self.group_seller_profile_tabs)
        return True

    @api.model
    def get_values(self):
        res = super(MarketplaceConfigSettings, self).get_values()
        group_seller_profile_tabs = self.env['ir.default'].sudo().get('res.config.settings', 'group_seller_profile_tabs')
        res.update({"group_seller_profile_tabs" : group_seller_profile_tabs})
        return res
