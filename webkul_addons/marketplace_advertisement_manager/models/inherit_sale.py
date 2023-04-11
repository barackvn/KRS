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

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    _order = 'ad_block_status'

    ad_display_type = fields.Selection(selection_add=[("ad_products", "Ad Products")])
    ad_product_ids = fields.Many2many("product.template", "ad_order_id", "product_tmplate_id", "ad")

    @api.onchange('ad_product_ids','ad_banner_img', 'ad_banner_link','ad_display_type')
    def _update_ad_content_status(self):
        res = super(SaleOrderLine, self)._update_ad_content_status()
        return

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        for rec in self:
            ad_display_type = vals.get("ad_display_type") or rec.ad_display_type
            if ad_display_type == "ad_products" and (
                vals.get("ad_product_ids")
                and vals.get("ad_product_ids")[0]
                and len(vals.get("ad_product_ids")[0][2]) < 3
                or len(rec.ad_product_ids) < 3
            ):
                raise UserError(_("Please add atleast 3 products for display type products."))
        return res
