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

class ResPartner(models.Model):
    _inherit = 'res.partner'

    seller_follower_ids = fields.One2many("marketplace.seller.followers", "marketplace_seller_id", "Seller Followers",copy=False,)
    seller_followers_count = fields.Integer(compute='_compute_seller_followers_count', string="Seller Followers Count")

    
    def _compute_seller_followers_count(self):
        for rec in self:
            rec.seller_followers_count = len(rec.seller_follower_ids)

    
    def action_seller_view_followers(self):
        self.ensure_one()
        action = self.env.ref('marketplace_favourite_seller.mp_seller_followers_action')
        list_view_id = self.env['ir.model.data'].xmlid_to_res_id(
            'marketplace_favourite_seller.mp_seller_followers_tree_view')
        form_view_id = self.env['ir.model.data'].xmlid_to_res_id(
            'marketplace_favourite_seller.mp_seller_followers_form_view')
        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[list_view_id, 'tree'], [form_view_id, 'form']],
            'view_mode': action.view_mode,
            'target': action.target,
            'res_model': action.res_model,
            'domain': f"[('marketplace_seller_id','=',{self._ids[0]}), ('active','=', True )]",
        }
