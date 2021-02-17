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

from odoo import api, fields, models
# import odoo.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class BannerImagesWizard(models.TransientModel):
    _name = "banner.images.wizard"
    _description = "Banner Images Wizard"

    partner_id = fields.Many2one("res.partner",'Seller')
    shop_id = fields.Many2one("seller.shop",'Seller Shop')
    banner_images = fields.Many2many("seller.banner.image")

    def write(self, vals):
        for rec in self:
            result = super(BannerImagesWizard,self).write(vals)
            if rec.partner_id:
                rec.partner_id.sudo().write({
                    'seller_banner_ids' : [(6, 0, rec.banner_images.ids)]
                })
            elif rec.shop_id:
                rec.shop_id.sudo().write({
                    'shop_banner_ids' : [(6, 0, rec.banner_images.ids)]
                })
            return result
