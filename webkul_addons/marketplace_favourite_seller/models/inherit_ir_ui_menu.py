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
from odoo import tools
import logging
_logger = logging.getLogger(__name__)

class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    
    def update_mp_menus(self, res):
        res = super(IrUiMenu, self).update_mp_menus(res)
        if self.env.user.has_group('odoo_marketplace.marketplace_seller_group') and not self.env.user.has_group('odoo_marketplace.marketplace_officer_group'):
            seller_menu_id = self.env['ir.model.data'].get_object_reference(
                'marketplace_favourite_seller', 'mp_seller_followers_menu')[1]
            for dictionary in res:
                if dictionary.get("id", False) == seller_menu_id:
                    dictionary["name"] = _("My Followers")
        return res
