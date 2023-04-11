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

class SellerShopStyle(models.Model):
    _inherit = "seller.shop"

    shop_banner_ids = fields.One2many('seller.banner.image','shop_id','Shop Slider Images')

    def get_seller_shop_banners(self):
        for rec in self:
            wiz_id = self.env["banner.images.wizard"].search([('shop_id','=',rec.id)],limit=1)
            if not wiz_id:
                wiz_id = self.env["banner.images.wizard"].sudo().create({
                    'shop_id': rec.id,
                    'banner_images': [(6, 0, rec.shop_banner_ids.ids)]
                })
            else:
                wiz_id.sudo().write({
                    'banner_images': [(6, 0, rec.shop_banner_ids.ids)]
                })
            return {
                'name': 'Seller Shop Banners',
                'type': 'ir.actions.act_window',
                'res_model': 'banner.images.wizard',
                'view_mode': 'form',
                'res_id': wiz_id.id,
                'view_id': self.env.ref(
                    'marketplace_seller_slider.banner_images_wizard_form_view'
                ).id,
                'context': self._context,
                'target': 'new',
            }
