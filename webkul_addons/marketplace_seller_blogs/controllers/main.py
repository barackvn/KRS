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
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.odoo_marketplace.controllers.main import MarketplaceSellerProfile
from odoo.addons.website_blog.controllers.main import WebsiteBlog
import logging
_logger = logging.getLogger(__name__)

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
        blog_post_obj = request.env['blog.post'].search([('marketplace_seller_id','=',seller_id),('website_published','=',True)])
        blog_url = QueryURL('', ['blog', 'tag'])
        response.qcontext.update({'blog_post_obj':blog_post_obj.sudo(),
            'blog_url'     :blog_url,
        })
        return response

class WebsiteBlog(WebsiteBlog):

    @http.route(['/blog/snippet/load'], type='json', auth="public", methods=['POST'], website=True)
    def blog_snippet_load(self, **post):
        blog_posts = request.env['blog.post'].search([
            ('marketplace_seller_id', '!=', False),
            ('is_published', '=', True)
            ], limit=5, order='post_date desc')
        values = {'blog_posts': blog_posts,}
        return request.env.ref("marketplace_seller_blogs.mp_blog_post_snippet_data").render(values, engine='ir.qweb')
