# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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


class WebsiteStock(http.Controller):

    @http.route('/website/stock_notify/', type='json', auth='public', website=True)
    def stock_notify(self, product_id, email, pageURL, name=None, **kwargs):
        if product_id:
            notify_obj = request.env['website.stock.notify'].sudo()
            record_create = notify_obj.create_stock_notify_record(int(product_id), email, request.uid, pageURL, name)
            return record_create
        return False
