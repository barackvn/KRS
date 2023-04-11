# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2016-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# License URL :<https://store.webkul.com/license.html/>
##########################################################################
from odoo import models,fields,api,_
from odoo.exceptions import Warning, UserError

import logging
_logger = logging.getLogger(__name__)

class SellerBannerImage(models.Model):
    _name = "seller.banner.image"
    _description = "Seller Banner Image"
    _order = "sequence"

    image = fields.Binary(string="Profile Banner", required=1, copy=False)
    sequence = fields.Integer(help="Determine the display order", default=1)
    url = fields.Char(string="URL")
    in_carousel = fields.Boolean(string='Show in Slider', default=True)
    partner_id = fields.Many2one('res.partner',String="Seller")
    shop_id = fields.Many2one('seller.shop',string="Shop")

    def write(self,vals):
        if vals.get('image') is None or vals.get('image'):
            return super(SellerBannerImage , self).write(vals)
        else:
            raise UserError('No image is uploaded in Slider image record, please upload it before saving.')

    @api.model
    def create(self,vals):
        if not vals.get('image'):
            raise UserError('No image is uploaded in Slider image record, please upload it before saving.')
        return super(SellerBannerImage , self).create(vals)
