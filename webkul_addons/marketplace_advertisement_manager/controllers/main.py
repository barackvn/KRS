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
from odoo.addons.website_advertisement_manager.controllers.main import WebsiteAdvertisement

class WebsiteAdvertisement(WebsiteAdvertisement):

    @http.route(['/set/block/banner'], method=['POST'], type='json', auth='public', website=True)
    def set_block_banner(self, block_id, image=None, ad_banner_link=None, ad_img_name=None, ad_display_type=None, ad_product_ids=None, **kw):
        res = super(WebsiteAdvertisement, self).set_block_banner(block_id, image, ad_banner_link, ad_img_name, **kw)
        block_line = request.env['sale.order.line'].sudo().browse(block_id)
        ad_display_type = ad_display_type if ad_display_type else "banner"
        if block_line:
            if ad_product_ids:
                block_line.ad_product_ids = [[6,0,ad_product_ids]]
            block_line.ad_display_type = ad_display_type
            block_line.ad_content_set_pending()
        return res
