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
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class MarketplaceSellerFollowers(models.Model):
    _name = "marketplace.seller.followers"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _rec_name = "customer_id"
    _description = "Marketplace Seller Followers"

    name = fields.Char(string="name")
    customer_id = fields.Many2one("res.partner", string="Customer", required=True,)
    customer_email = fields.Char("Customer Email", related="customer_id.email",)
    marketplace_seller_id = fields.Many2one("res.partner", string="Seller", required=True,)
    desc = fields.Text("Description")
    active = fields.Boolean("Is a Follower", default=True)

    _sql_constraints = [
        ('mp_customer_fav_seller_uniq', 'unique (customer_id, marketplace_seller_id)',
        _('There is already a record for this customer with this seller.'))
    ]

    def toggle_active(self):
        for record in self:
            record.active = not record.active

    @api.model
    def create(self, vals):
        res= super(MarketplaceSellerFollowers, self).create(vals)
        if vals.get("customer_id") and vals.get("marketplace_seller_id"):
            if vals.get("customer_id") == vals.get("marketplace_seller_id"):
                raise UserError(_("Customer and Seller cannot be same"))
        # res._add_customer_in_mail_followers(vals.get("customer_id"))
        return res


    def write(self, vals):
        res= super(MarketplaceSellerFollowers, self).write(vals)
        for rec in self:
            customer_id = vals.get("customer_id") if vals.get("customer_id") else rec.customer_id.id
            marketplace_seller_id = vals.get("marketplace_seller_id") if vals.get("marketplace_seller_id") else rec.marketplace_seller_id.id
            if customer_id == marketplace_seller_id:
                raise UserError(_("Customer and Seller cannot be same"))
        return res


    def action_send_email_to_seller_followers(self):
        composer_form_view_id = self.env.ref('marketplace_favourite_seller.mp_fav_seller_email_compose_message_wizard_form').id
        try:
            default_template = self.env.ref('marketplace_favourite_seller.mp_fav_seller_email_template_info', raise_if_not_found=False)
            template_id = default_template.id if default_template else False

        except:
            template_id = False
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'view_id': composer_form_view_id,
            'target': 'new',
            'context': {
                'multiple_rec': 'yes' if len(self) > 1 else 'no',
                'default_composition_mode': 'mass_mail',
                'default_res_id': self.ids[0],
                'default_model': 'marketplace.seller.followers',
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'website_sale_send_recovery_email': True,
                'active_ids': self.ids,
            },
        }

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    access_token = fields.Char('Access Token', groups="base.group_user,odoo_marketplace.marketplace_seller_group")
