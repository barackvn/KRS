# -*- coding: utf-8 -*-
##########################################################################
# 2010-2017 Webkul.
#
# NOTICE OF LICENSE
#
# All right is reserved,
# Please go through this link for complete license : https://store.webkul.com/license.html
#
# DISCLAIMER
#
# Do not edit or add to this file if you wish to upgrade this module to newer
# versions in the future. If you wish to customize this module for your
# needs please refer to https://store.webkul.com/customisation-guidelines/ for more information.
#
# @Author        : Webkul Software Pvt. Ltd. (<support@webkul.com>)
# @Copyright (c) : 2010-2017 Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# @License       : https://store.webkul.com/license.html
#
##########################################################################

from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

SPG = 20

class MarketplaceSellerStory(http.Controller):

    @http.route(['/seller/story/<int:seller_story_id>'], type='http', auth="public", website=True)
    def seller_story_page(self, seller_story_id, **post):
        if not seller_story_id:
            return False
        seller_story_obj = request.env["seller.story"].sudo().browse(seller_story_id)
        return request.render("marketplace_seller_story.mp_seller_story_page", {'story': seller_story_obj})


    @http.route(['/seller/story/', '/seller/story/page/<int:page>'], type='http', auth="public", website=True)
    def seller_story(self, page=0, spg=False, **post):
        url = "/seller/story/"
        if spg:
            try:
                spg = int(spg)
            except ValueError:
                spg = SPG
            post["spg"] = spg
        else:
            spg = SPG
        selelr_story = request.env["seller.story"]
        domain = [("website_published", "=", True), ("seller_id.state", "=", "approved")]
        seller_story_count = selelr_story.sudo().search_count(domain)
        pager = request.website.pager(url=url, total=seller_story_count, page=page, step=spg, scope=7, url_args=post)
        seller_story_objs = selelr_story.sudo().search(domain, limit=spg, offset=pager['offset'], order='id desc')
        popular_stories = selelr_story.sudo().search(domain + [("is_popular", "=", True)])
        values = {
            'seller_stories': seller_story_objs,
            'pager': pager,
            'popular_stories': popular_stories,
        }
        return request.render("marketplace_seller_story.mp_seller_stories_page", values)
