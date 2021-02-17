# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

import logging
_logger = logging.getLogger(__name__)


class website_sale(WebsiteSale):

    @http.route(['/website/order/notes'], type='json', auth="public", website=True)
    def order_notes(self, notes='', desire_date=False, **post):
        _logger.info("-----------notes------%r",notes)
        _logger.info("-----------desire_date------%r",desire_date)
        order = request.website.sale_get_order()
        order.sudo().write(
            {'wk_notes': notes, 'wk_desire_date': desire_date})
        return True
