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
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    allow_seller_for_360degree_view = fields.Boolean(
        string= 'Allow Seller for 360 degree view',
        compute= "_get_360degree_info_for_seller",
        )

    def _get_360degree_info_for_seller(self):
        for obj in self:
            obj.allow_seller_for_360degree_view = False
            seller_360degree_group = self.env.ref('marketplace_360degree_view.group_for_mp_360degree_view')
            user_obj = self.env["res.users"].sudo().search([('partner_id', '=', obj.id)])
            user_groups = user_obj.read(['groups_id'])
            if user_groups and user_groups[0].get("groups_id"):
                user_groups_ids = user_groups[0].get("groups_id")
                if seller_360degree_group.id in user_groups_ids:
                    obj.allow_seller_for_360degree_view = True
            else:
                obj.allow_seller_for_360degree_view = False

    def enable_seller_360degree_group(self):
        for obj in self:
            if (
                user := self.env["res.users"]
                .sudo()
                .search([('partner_id', '=', obj.id)])
            ):
                if group := self.env.ref(
                    'marketplace_360degree_view.group_for_mp_360degree_view'
                ):
                    group.sudo().write({"users": [(4, user.id, 0)]})

    def disable_seller_360degree_group(self):
        for obj in self:
            if (
                user := self.env["res.users"]
                .sudo()
                .search([('partner_id', '=', obj.id)])
            ):
                if group := self.env.ref(
                    'marketplace_360degree_view.group_for_mp_360degree_view'
                ):
                    group.sudo().write({"users": [(3, user.id, 0)]})
                    # disbale 360 view on website
                    user_products = self.env["product.template"].sudo().search([('marketplace_seller_id', '=', obj.id)])
                    for product in user_products:
                        product.product_default_view = True
                        product.product_360_view = False
