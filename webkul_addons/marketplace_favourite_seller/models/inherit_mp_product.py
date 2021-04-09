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
import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    
    def toggle_website_published(self):
        res = super(ProductTemplate, self).toggle_website_published()
        notify_follower_on_new_product = self.env['res.config.settings'].sudo().get_values().get('enable_notify_follower_on_new_product')
        template_id = self.env['res.config.settings'].sudo().get_values().get("notify_follower_on_new_product_mail_template")
        if template_id:
            template_id = self.env['mail.template'].browse(template_id)
        else:
            self.sudo().env.ref("marketplace_favourite_seller.mp_fav_seller_email_template_to_followers")
        if notify_follower_on_new_product and template_id:
            for rec in self:
                if rec.website_published and rec.marketplace_seller_id and rec.marketplace_seller_id.seller_follower_ids:
                    [template_id.send_mail(follower.id ,force_send=True) for follower in rec.marketplace_seller_id.seller_follower_ids]
        return res
