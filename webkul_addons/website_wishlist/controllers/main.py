# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteWishlist(WebsiteSale):

    # def get_attribute_values_dict(self, product):
    #     variant_attribute_values_dict = dict()
    #     for value_id in product.attribute_value_ids:
    #         variant_attribute_values_dict[value_id.attribute_id.id] = value_id.id
    #     return variant_attribute_values_dict
   

    @http.route(['/wishlist'], type='http', auth="public", website=True)
    def wk_wishlist(self, **post):
        values = {
            'wishlist': request.env['website.wishlist'].get_wishlist_products(),
            # 'get_attribute_exclusions': self._get_attribute_exclusions,
            }
        if request.website.is_public_user():
            return request.redirect('/shop')
        return http.request.render("website_wishlist.wishlist", values)


    @http.route('/wishlist/add_to_wishlist', type='json', auth='public', website=True)
    def wk_add_to_wishlist(self, product, *args, **kwargs):
        add = request.env['res.users'].add_product(int(product))
        return add

    @http.route('/wishlist/remove_from_wishlist', type='json', auth='public', website=True)
    def wk_remove_from_wishlist(self, product, *args, **kwargs):
        remove = request.env['res.users'].remove_product(int(product))
        return remove


    @http.route(['/wishlist/move_to_cart'], type='json', auth="public", methods=['POST'], website=True)
    def wk_move_to_cart(self, product_id, line_id=None, add_qty=1, set_qty=None, display=True):
        # remove from wishlist part is missing
        order = request.website.sale_get_order(force_create=1)
        value = order._cart_update(product_id=int(product_id), line_id=line_id, add_qty=add_qty, set_qty=set_qty)
        if not display:
            return None
        value['cart_quantity'] = order.cart_quantity
        value['website_sale.total'] = request.website._render("website_sale.total", {
                'website_sale_order': request.website.sale_get_order()
            })
        return value
