# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def merge_in_exist_order(self, selectedOrdrs, mergingOrder, actionType):
        text = 'Order merged successfully'
        try:
            filterOrder = selectedOrdrs - mergingOrder
            for poLine in filterOrder.mapped('order_line'):
                copyLine = poLine.copy()
                copyLine.order_id = mergingOrder.id
            filterOrder.button_cancel()
            if actionType == 'merge_exist_delete_other':
                filterOrder.unlink()
        except Exception as e:
            text = 'Failed to merge: \nError : {}'.format(str(e))
        return text

    @api.model
    def merge_create_order(self, selectedOrdrs, actionType, parnterIds):
        text = 'Order merged successfully'
        try:
            purchaseOrder = self.create({'partner_id': parnterIds[0]})
            purchaseOrder.onchange_partner_id()
            for poLine in selectedOrdrs.mapped('order_line'):
                copyLine = poLine.copy()
                copyLine.order_id = purchaseOrder.id
            selectedOrdrs.button_cancel()
            if actionType == 'merge_delete':
                selectedOrdrs.unlink()
            purchaseOrder._amount_all()
        except Exception as e:
            text = 'Failed to merge: \nError : {}'.format(str(e))
        return text
