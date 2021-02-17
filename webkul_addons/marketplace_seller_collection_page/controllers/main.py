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
import logging
logger = logging.getLogger(__name__)


class MarketplaceSellerProfile(MarketplaceSellerProfile):

    @http.route(['/seller/profile/<int:seller_id>',
        '/seller/profile/<int:seller_id>/page/<int:page>',
        '/seller/profile/<seller_url_handler>',
        '/seller/profile/<seller_url_handler>/page/<int:page>'],
        type='http', auth="public", website=True)
    def seller(self, seller_id=None, seller_url_handler=None, page=0, category=None, search='', ppg=False, **post):
        response = super(MarketplaceSellerProfile, self).seller(seller_id, seller_url_handler, page, category, search, ppg, **post)
        if response.qcontext.get('seller'):
            seller_obj = response.qcontext.get('seller')
            seller_id = seller_obj.id
        collec_page_obj = request.env['website.collectional.page'].search([('marketplace_seller_id','=',seller_id),('state','=','pub')])
        collec_group_obj = request.env['website.collectional.group'].search([('marketplace_seller_id','=',seller_id),('state','=','published')])
        response.qcontext.update({'collections_page':collec_page_obj.sudo(),
                                  'collections_group':collec_group_obj.sudo(),
                                })
        return response
