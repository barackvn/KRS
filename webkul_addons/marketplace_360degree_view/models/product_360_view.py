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

from odoo import api, fields, models, tools, _
import logging
_logger = logging.getLogger(__name__)

class Product360View(models.Model):
    _inherit = 'product.360.view'

    marketplace_seller_id = fields.Many2one("res.partner", string="Seller", related='template_id.marketplace_seller_id', default=False)
