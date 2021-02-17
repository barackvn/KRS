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


from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create_seller_payment_new(self, sellers_dict):
        voucher_product_id = self.env['ir.default'].sudo().get('res.config.settings', 'wk_coupon_product_id')
        invoice_id = sellers_dict.get('invoice_id',False)
        if invoice_id:
            invoice_obj = self.browse(int(invoice_id))
            if invoice_obj and invoice_obj.type in ['out_invoice', 'out_refund']:
                voucher_inv_line = invoice_obj.invoice_line_ids.filtered(lambda l: l.product_id.id == voucher_product_id)
                order = self.env["sale.order"].search([('name','=',invoice_obj.invoice_origin)],limit=1)
                voucher_obj = order.applied_voucher if order.applied_voucher else False
                if voucher_inv_line and voucher_obj and voucher_obj.marketplace_seller_id:
                    #  update a inv line of the seller whose voucher has been applied_voucher
                    for seller_id in sellers_dict.get("seller_ids"):
                        if seller_id == voucher_obj.marketplace_seller_id.id:
                            voucher_seller_dict = sellers_dict.get("seller_ids")[voucher_obj.marketplace_seller_id.id]
                            voucher_seller_dict["invoice_line_payment"].append(voucher_inv_line.price_unit)
                            voucher_seller_dict["invoice_line_ids"].append(voucher_inv_line.id)
        res = super(AccountMove, self).create_seller_payment_new(sellers_dict)
        return res
