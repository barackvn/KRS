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

from odoo import http, _
from odoo.addons.website_advertisement_manager.controllers.portal import PortalAccount
from odoo.http import request

class PortalAccount(PortalAccount):

    @http.route(['/my/ad/blocks/<int:ad_block_id>'], type='http', auth="user", website=True)
    def portal_my_ad_block_detail(self, ad_block_id=None, access_token=None, **kw):
        res = super(PortalAccount, self).portal_my_ad_block_detail(ad_block_id, access_token, **kw)
        domain = [
            ("website_published",'=',True),
            ("sale_ok", '=', True),
            ("is_ad_block",'=', False),
        ]
        if request.env.user and request.env.user.partner_id.seller:
            domain += [("marketplace_seller_id", "=", request.env.user.partner_id.id),("status", "=", "approved"),]
        ad_products = request.env['product.template'].search(domain)
        res.qcontext.update({
            'ad_products': ad_products,
        })
        return res
