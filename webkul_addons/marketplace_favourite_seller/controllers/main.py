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
from odoo.addons.odoo_marketplace.controllers.main import MarketplaceSellerProfile
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging
_logger = logging.getLogger(__name__)
try:
    import urlparse
    from urllib import urlencode
except: # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode

class MarketplaceFavouriteSeller(http.Controller):

    @http.route(['/add/favourite'], type='http', auth='public', website=True,)
    def _add_favourite_seller(self, **kwargs):
        customer_id = request.env.user.partner_id.id
        seller_id = int(kwargs.get("marketplace_seller_id"))
        values = {
            'customer_id': customer_id,
            'marketplace_seller_id': seller_id,
        }
        FavSeller = request.env['marketplace.seller.followers'].sudo()
        # url = request.httprequest.referrer
        url = "/my/favourite/sellers"

        params = {}
        # search if a record already exist
        if FavSeller.search([('customer_id', '=',customer_id),('marketplace_seller_id', '=',seller_id),('active', '=', True)]):
            params = {'add_favourite_error':1}
        elif FavSeller.search([('customer_id', '=',customer_id),('marketplace_seller_id', '=',seller_id),('active', '=', False)]):
            params = {'add_favourite_success':1}
            fav_seller_exist = FavSeller.search([('customer_id', '=',customer_id),('marketplace_seller_id', '=',seller_id),('active', '=', False)])
            fav_seller_exist.sudo().active = True
        else:
            try:
                FavSeller.sudo().create(values)
                params = {'add_favourite_success':1}
            except:
                params = {'add_favourite_error':1}

        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        if query.get("add_favourite_success") or query.get("add_favourite_error"):
            pass
        else:
            query.update(params)
        url_parts[4] = urlencode(query)
        url = urlparse.urlunparse(url_parts)

        return request.redirect(url)

    @http.route(['/remove/favourite'], type='http', auth='public', website=True,)
    def _remove_favourite_seller(self, **kwargs):
        # url = request.httprequest.referrer
        url = "/my/favourite/sellers"
        customer_id = request.env.user.partner_id.id
        seller_id = int(kwargs.get("marketplace_seller_id"))
        FavSeller = request.env['marketplace.seller.followers'].sudo()
        fav_seller_obj = FavSeller.search([('customer_id', '=',customer_id),('marketplace_seller_id', '=',seller_id),('active', '=', True)])
        if fav_seller_obj:
            fav_seller_obj.sudo().active = False
            url = url + "?seller_remove_success=1"
        return request.redirect(url)
