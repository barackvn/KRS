# -*- coding: utf-8 -*-
##########################################################################
# 2010-2017 Webkul.
#
# NOTICE OF LICENSE
#
# All right is reserved,
# Please go through this link for complete license : https://store.webkul.com/license.html
#
# DISCLAIMER
#
# Do not edit or add to this file if you wish to upgrade this module to newer
# versions in the future. If you wish to customize this module for your
# needs please refer to https://store.webkul.com/customisation-guidelines/ for more information.
#
# @Author        : Webkul Software Pvt. Ltd. (<support@webkul.com>)
# @Copyright (c) : 2010-2017 Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# @License       : https://store.webkul.com/license.html
#
##########################################################################

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class MarketplacePreorderConfigSettings(models.Model):
    _inherit = 'website.preorder.config.settings'

    preorder_for_seller = fields.Boolean(string="Allow pre-order for seller",help="")

    @api.model
    def assign_preorder_to_seller(self):
        preorder_group_id = self.env['ir.model.data'].get_object_reference('website_preorder', 'website_preorder_group')[1]
        implied_group_id = self.env['ir.model.data'].get_object_reference('odoo_marketplace', 'marketplace_seller_group')[1]
        groups_obj = self.env["res.groups"].browse(preorder_group_id)
        implied_groups = self.env["res.groups"].browse(implied_group_id)
        implied_groups.sudo().write({'implied_ids':[(4,preorder_group_id)]})

    @api.model
    def remove_preorder_from_seller(self):
        preorder_group_id = self.env['ir.model.data'].get_object_reference('website_preorder', 'website_preorder_group')[1]
        implied_group_id = self.env['ir.model.data'].get_object_reference('odoo_marketplace', 'marketplace_seller_group')[1]
        groups_obj = self.env["res.groups"].browse(preorder_group_id)
        implied_groups = self.env["res.groups"].browse(implied_group_id)
        implied_groups.sudo().write({'implied_ids':[(3,preorder_group_id)]})
        groups_obj.sudo().write({'users': [(3, user.id) for user in implied_groups.mapped('users').filtered('partner_id.seller')]})


    def write(self, vals):
        res = super(MarketplacePreorderConfigSettings, self).write(vals)
        active_ids = self.search([('is_active', '=', True)])
        for rec in self:
            if 'is_active' in vals:
                if vals.get('is_active'):
                    if 'preorder_for_seller' in vals:
                        if vals.get('preorder_for_seller'):
                            rec.assign_preorder_to_seller()
                        else:
                            rec.remove_preorder_from_seller()
                    else:
                        if rec.preorder_for_seller:
                            rec.assign_preorder_to_seller()
                        else:
                            rec.remove_preorder_from_seller()
                elif len(active_ids) == 0:
                    rec.remove_preorder_from_seller()
            elif rec.is_active and 'preorder_for_seller' in vals:
                if vals.get('preorder_for_seller'):
                    rec.assign_preorder_to_seller()
                else:
                    rec.remove_preorder_from_seller()

        return res

    @api.model
    def create(self, vals):
        if vals.get('is_active') and vals.get('preorder_for_seller'):
            self.assign_preorder_to_seller()
        return super(MarketplacePreorderConfigSettings, self).create(vals)
