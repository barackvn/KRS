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

    enable_notify_follower_on_new_product = fields.Boolean(string="Enable to Send Mail To Follower on New Seller Product")
    notify_follower_on_new_product_mail_template = fields.Many2one(
        "mail.template", string="Notification for Follower", domain="[('model_id.model','=','marketplace.marketplace.favourite.seller')]")

    def set_values(self):
        super(MarketplaceConfigSettings, self).set_values()
        IrDefault = self.env['ir.default'].sudo()
        IrDefault.set('res.config.settings', 'enable_notify_follower_on_new_product', self.enable_notify_follower_on_new_product)
        IrDefault.set('res.config.settings', 'notify_follower_on_new_product_mail_template', self.notify_follower_on_new_product_mail_template.id)
        return True

    @api.model
    def get_values(self, fields=None):
        res = super(MarketplaceConfigSettings, self).get_values()
        notify_follower_on_new_product_mail_template = self.env['ir.model.data'].get_object_reference(
            'marketplace_favourite_seller', 'mp_fav_seller_email_template_to_followers')[1]
        IrDefault = self.env['ir.default'].sudo()
        res.update({
            'enable_notify_follower_on_new_product': IrDefault.get('res.config.settings', 'enable_notify_follower_on_new_product'),
            'notify_follower_on_new_product_mail_template': IrDefault.get('res.config.settings', 'notify_follower_on_new_product_mail_template')
                or notify_follower_on_new_product_mail_template,
        })
        return res
