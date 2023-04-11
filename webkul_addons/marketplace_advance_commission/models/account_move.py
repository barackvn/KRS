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
from odoo.exceptions import UserError
from odoo.http import request
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    def calculate_commission(self, list_price, seller_id, invoice_line_obj=None):
        """ Calculates the commission as defined in the marketplace configuration with commission type.
            Param price_unit gives the price after deducting the commission and
            Param comm_factor gives the total commission deducted from list_price """
        price_unit = 0
        comm_factor = 0
        config_setting_obj = self.env[
            'res.config.settings'].get_values()
        comm_type = config_setting_obj.get('comm_type')
        category_comm = config_setting_obj.get('category_comm')
        mp_config_currency = self.env['res.currency'].search([('id','=',config_setting_obj.get('mp_currency_id'))])
        if len(mp_config_currency) == 0 :
            mp_config_currency = self.env['res.currency'].search([('id', '=', self.company_id.currency_id.id)])
        sale_order_obj = self.env['sale.order'].search([('name','=',self.invoice_origin)])
        seller_obj = self.env["res.partner"].browse(seller_id)

        if comm_type == 'product' and invoice_line_obj:
            invoice_line_obj.commission_type = "Product"
            if invoice_line_obj.product_id.comm_method:
                product = invoice_line_obj.product_id
                return self.convert_currency_n_calc_comm(
                    product.comm_method,
                    list_price,
                    invoice_line_obj.quantity,
                    product.percent_commission,
                    product.fix_commission,
                    product.currency_id,
                    sale_order_obj.currency_id,
                    invoice_line_obj,
                )
            if invoice_line_obj.product_id.public_categ_ids:
                comm_list = []
                for category in invoice_line_obj.product_id.public_categ_ids:
                    if category.comm_method:
                        price = self.convert_currency_n_calc_comm(category.comm_method, list_price, invoice_line_obj.quantity, category.percent_commission, category.fix_commission, mp_config_currency, sale_order_obj.currency_id, invoice_line_obj)
                        comm_list.append(price)
                if comm_list != []:
                    price_unit = max(comm_list) if category_comm == 'minimum' else min(comm_list)
                    # code updated for showing in wizard the correct category commission if product has multiple category
                    if len(invoice_line_obj.product_id.public_categ_ids)>1:
                        self._get_applied_mp_categ_comm_details(list_price, invoice_line_obj.quantity, mp_config_currency, sale_order_obj.currency_id, invoice_line_obj)

                    return price_unit

            price_unit = self.convert_currency_n_calc_comm(seller_obj.get_seller_global_fields('comm_method'), list_price, invoice_line_obj.quantity, seller_obj.get_seller_global_fields('commission'), seller_obj.get_seller_global_fields('fix_commission'), mp_config_currency, sale_order_obj.currency_id, invoice_line_obj)
            return price_unit

        if comm_type == 'category' and invoice_line_obj:
            invoice_line_obj.commission_type = "Category"
            if invoice_line_obj.product_id.public_categ_ids:
                comm_list = []
                for category in invoice_line_obj.product_id.public_categ_ids:
                    if category.comm_method:
                        price = self.convert_currency_n_calc_comm(category.comm_method, list_price, invoice_line_obj.quantity, category.percent_commission, category.fix_commission, mp_config_currency, sale_order_obj.currency_id, invoice_line_obj)
                        comm_list.append(price)
                if comm_list != []:
                    price_unit = max(comm_list) if category_comm == 'minimum' else min(comm_list)
                    # code updated for showing in wizard the correct category commission if product has multiple category
                    if len(invoice_line_obj.product_id.public_categ_ids)>1:
                        self._get_applied_mp_categ_comm_details(list_price, invoice_line_obj.quantity, mp_config_currency, sale_order_obj.currency_id, invoice_line_obj)

                    return price_unit

            if invoice_line_obj.product_id.comm_method:
                product = invoice_line_obj.product_id
                price_unit = self.convert_currency_n_calc_comm(product.comm_method, list_price, invoice_line_obj.quantity, product.percent_commission, product.fix_commission, product.currency_id, sale_order_obj.currency_id, invoice_line_obj)
                return price_unit

            price_unit = self.convert_currency_n_calc_comm(seller_obj.get_seller_global_fields('comm_method'), list_price, invoice_line_obj.quantity, seller_obj.get_seller_global_fields('commission'), seller_obj.get_seller_global_fields('fix_commission'), mp_config_currency, sale_order_obj.currency_id, invoice_line_obj)
            return price_unit

        if comm_type == 'seller' and invoice_line_obj:
            invoice_line_obj.commission_type = "Seller"
            price_unit = self.convert_currency_n_calc_comm(seller_obj.get_seller_global_fields('comm_method'), list_price, invoice_line_obj.quantity, seller_obj.get_seller_global_fields('commission'), seller_obj.get_seller_global_fields('fix_commission'), mp_config_currency, sale_order_obj.currency_id, invoice_line_obj)
            return price_unit
        return price_unit


    def convert_currency_n_calc_comm(self, comm_method, list_price, qty, percent_comm, fix_comm, from_currency, to_currency, invoice_line_obj=None):
        fix_comm = from_currency.compute(fix_comm, to_currency)
        price_unit = 0
        if comm_method:

            invoice_line_obj.comm_method = comm_method
            invoice_line_obj.fix_comm = fix_comm
            invoice_line_obj.perc_comm = percent_comm

            # Case Percent commission
            if comm_method == 'percent' :
                comm_factor = (list_price * (percent_comm / 100.0))
                price_unit = list_price - comm_factor

            # Case Fix Commission
            elif comm_method == 'fix' :
                comm_factor = fix_comm * qty
                price_unit = list_price - comm_factor

            # Case Percent+Fix Commission
            elif comm_method == 'percent_and_fix' :
                    percent_comm = (list_price * (percent_comm / 100.0))
                    comm_factor = percent_comm + (fix_comm * qty)
                    price_unit = list_price - comm_factor

            # Case Fix+Percent Commission
            elif comm_method == 'fix_and_percent' :
                    new_price = list_price - (fix_comm * qty)
                    percent_comm = (new_price * (percent_comm / 100.0))
                    comm_factor = percent_comm + fix_comm
                    price_unit = new_price - percent_comm

        return price_unit


    def _get_applied_mp_categ_comm_details(self, list_price, qty, from_currency, to_currency, invoice_line_obj):
        category_comm = self.env['res.config.settings'].get_values().get('category_comm')
        comm_factor_list = []
        if invoice_line_obj:
            for category in invoice_line_obj.product_id.public_categ_ids:
                percent_comm = category.percent_commission
                comm_factor = 0
                if comm_method := category.comm_method:
                    fix_comm = from_currency.compute(category.fix_commission, to_currency)
                    if comm_method == 'fix':
                        comm_factor = fix_comm * qty
                    elif comm_method == 'fix_and_percent':
                        new_price = list_price - (fix_comm * qty)
                        percent_comm = (new_price * (percent_comm / 100.0))
                        comm_factor = percent_comm + fix_comm
                    elif comm_method == 'percent':
                        comm_factor = (list_price * (percent_comm / 100.0))
                    elif comm_method == 'percent_and_fix':
                        percent_comm = (list_price * (percent_comm / 100.0))
                        comm_factor = percent_comm + (fix_comm * qty)
                    comm_factor_list.append((comm_factor,category.comm_method,category.fix_commission, category.percent_commission))
            if comm_factor_list != []:
                item = (
                    min(comm_factor_list, key=lambda t: t[0])
                    if category_comm == 'minimum'
                    else max(comm_factor_list, key=lambda t: t[0])
                )
                invoice_line_obj.perc_comm = item[3]
                invoice_line_obj.fix_comm = item[2]
                invoice_line_obj.comm_method = item[1]
        return

    def create_seller_invoice_new(self):
        for invoice_obj in self:
            if invoice_obj.type in ['out_invoice', 'out_refund']:
                sellers = {"seller_ids": {}}
                for invoice_line_obj in invoice_obj.invoice_line_ids:
                    seller_id = invoice_line_obj.product_id.marketplace_seller_id.id if invoice_line_obj.product_id.marketplace_seller_id else False
                    if seller_id:
                        seller_amount = self.calculate_commission(invoice_line_obj.price_subtotal, seller_id, invoice_line_obj)
                        invoice_line_obj.seller_commission = invoice_line_obj.price_subtotal - seller_amount
                        if sellers["seller_ids"].get(seller_id, False):
                            # ADD all product
                            sellers["seller_ids"][seller_id]["invoice_line_payment"].append(seller_amount)
                            sellers["seller_ids"][seller_id]["invoice_line_ids"].append(invoice_line_obj.id)
                        else:
                            sellers["seller_ids"].update({
                                    seller_id : {
                                        "invoice_line_payment": [seller_amount],
                                        "invoice_line_ids": [invoice_line_obj.id],
                                    }
                                }
                            )
                sellers |= {
                    "invoive_type": invoice_obj.type,
                    "invoice_id": invoice_obj.id,
                    "invoice_currency": invoice_obj.currency_id,
                    "payment_mode": "order_paid"
                    if invoice_obj.type == "out_invoice"
                    else "order_refund",
                    "description": _("Order Invoice Payment")
                    if invoice_obj.type == "out_invoice"
                    else _("Order Invoice Refund"),
                    "payment_type": "cr"
                    if invoice_obj.type == "out_invoice"
                    else "dr",
                    "state": "draft",
                    "memo": invoice_obj.invoice_origin or invoice_obj.name,
                }
                self.create_seller_payment_new(sellers)

class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    commission_type = fields.Char("Commission Type", readonly=True)
    comm_method = fields.Char("Commission Method", readonly=True)
    perc_comm = fields.Float("Percent Commission")
    fix_comm = fields.Float("Fixed Commission")

    def button_view_comm_details(self):
        if self.comm_method and self.commission_type:
            currency_symbol = self.currency_id.symbol if self.currency_id else ''
            if self.comm_method == 'fix':
                desc = "Fixed Commission" + " : " + str(self.fix_comm) + currency_symbol + " = " + str(self.seller_commission)
            elif self.comm_method == 'fix_and_percent':
                desc = "Fix + Percent Commission" + " : "  + str(self.fix_comm) + currency_symbol + " + " + str(self.perc_comm) + "%" + " = " + str(self.seller_commission)
            elif self.comm_method == 'percent':
                desc = "Percent Commission" + " : " + str(self.perc_comm) + "%" + " = " + str(self.seller_commission)
            elif self.comm_method == 'percent_and_fix':
                desc = "Percent + Fixed Commission" + " : " + str(self.perc_comm) + "% + " + str(self.fix_comm) + currency_symbol + " = " + str(self.seller_commission)
            desc = f"{desc} ({str(self.commission_type)} Commission)"
        else:
            desc = ''
        view_id= self.env["commtype.desc.wizard"].create({'desc': desc,})
        return {
            'name': _("Description of Commission"),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'commtype.desc.wizard',
            'res_id': view_id.id,
            'type': "ir.actions.act_window",
            'target': 'new',
        }
