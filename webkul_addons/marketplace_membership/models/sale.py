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

from odoo import api, models, fields, tools, _
import logging
_logger = logging.getLogger(__name__)



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def is_order_has_already_membership(self):
        self.ensure_one()
        line_with_membership_product = 0
        for line in self.order_line:
            if line.product_id.wk_mp_membership:
                line_with_membership_product = line.product_id.id
        return line_with_membership_product

  
    def _website_product_id_change(self, order_id, product_id, qty=0):
        order = self.sudo().browse(order_id)
        res = super(SaleOrder, self)._website_product_id_change(order_id, product_id, qty)
        product_obj = self.env['product.product'].browse(product_id)
        if order.is_order_has_already_membership() and order.is_order_has_already_membership() !=product_id and product_obj.wk_mp_membership:
            res.update({"product_uom_qty" : 0})
        return res
