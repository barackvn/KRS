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

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging
_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):

    @http.route(['/shop/cart/update_cart_voucher'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_cart_voucher(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True):
        order = request.website.sale_get_order()
        secret_code = request.session.get('secret_key_data')
        if secret_code:
            if set_qty == 0:
                product_obj = request.env['product.product'].search([('id','=',product_id)])
                if product_obj.marketplace_seller_id :
                    count = 0
                    for line in order.order_line:
                        if line.product_id.marketplace_seller_id:
                            if line.product_id.marketplace_seller_id == product_obj.marketplace_seller_id :
                                count = count+1

                    if count == 1:
                        voucher_product_id = request.env['ir.default'].sudo().get('res.config.settings', 'wk_coupon_product_id')
                        for line in order.order_line:
                            if line.product_id.id == voucher_product_id:
                                secret_code = request.session.get('secret_key_data')
                                voucher_obj = request.env['voucher.voucher'].search([('id','=',secret_code.get('coupon_id'))])
                                if voucher_obj.marketplace_seller_id == product_obj.marketplace_seller_id:
                                    line.sudo().unlink()
                                    return voucher_product_id
        return True
