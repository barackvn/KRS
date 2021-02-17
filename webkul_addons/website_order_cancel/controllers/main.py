# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################

from odoo import http
from odoo.http import request
from odoo import SUPERUSER_ID
from odoo.addons.website_sale.controllers.main import WebsiteSale

import logging
_logger = logging.getLogger(__name__)


class website_sale(WebsiteSale):

    @http.route(['/cancel/order'], type='json', auth="public", methods=['POST'], website=True)
    def quick_cancel(self, order_id, view_type,  **kwargs):
        order_obj = request.env['sale.order']
        reasons = request.env['order.cancel.reason'].search([])
        order = order_obj.browse(int(order_id))
        return request.env['ir.ui.view'].render_template("website_order_cancel.modal_cancel_order", {
            'main_object': order,
            'order': order,
            'reasons': reasons,
            'view_type': view_type
        })

    @http.route(['/cancel/order/confirm'], type='json', auth="public", methods=['POST'], website=True)
    def quick_cancel_confirm(self, order_id, reason_id, remark, **kwargs):
        order_obj = request.env['sale.order']
        order = order_obj.sudo().browse(int(order_id))
        order.action_cancel()
        last_tx_id = order.get_portal_last_transaction()
        if last_tx_id and last_tx_id.state in ['draft', 'pending']:
            last_tx_id.state = 'cancel'
        order.write({'reason_id': reason_id, 'additional_remark': remark})
        return True
