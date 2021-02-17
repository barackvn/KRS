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

from odoo import SUPERUSER_ID
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import QueryURL


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/360view/'], type='json', auth="public", methods=['POST'], website=True)
    def product_360view_modal(self, product_id, **kwargs):
        product_obj = request.env['product.template']
        if product_id:
            product = product_obj.sudo().browse(product_id)
        return request.env['ir.ui.view'].render_template("website_360degree_view.modal_product_360degree_view", {
            'product': product if product else request.env['product.template'],
        })
