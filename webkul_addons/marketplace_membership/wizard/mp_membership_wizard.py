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

from odoo import api, fields, models

class MarketplaceMembershipInvoice(models.TransientModel):
    _name = "mp.membership.invoice"
    _description = "Marketplace Membership Invoice"

    product_id = fields.Many2one('product.product', string='Membership', required=True, domain="[('wk_mp_membership', '=', True)]")
    membership_fee = fields.Float(string='Membership Price', digits= 'Product Price', required=True)

    @api.onchange('product_id')
    def onchange_product(self):
        """Return value of  product's membership fee based on product id."""
        price_dict = self.product_id.price_compute('list_price')
        self.membership_fee = price_dict.get(self.product_id.id) or False

    def create_seller_membership_invoice(self):
        if self:
            datas = {
                'membership_product_id': self.product_id.id,
                'amount': self.membership_fee
            }
        invoice_list = self.env['res.partner'].browse(self._context.get('active_ids')).create_mp_membership_invoice(datas=datas)

        search_view_ref = self.env.ref('account.view_account_invoice_filter', False)
        form_view_ref = self.env.ref('account.view_move_form', False)

        return  {
            'domain': [('id', 'in', invoice_list)],
            'name': 'Membership Invoices',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'views': [(False, 'tree'), (form_view_ref and form_view_ref.id, 'form')],
            'search_view_id': search_view_ref and search_view_ref.id,
        }
