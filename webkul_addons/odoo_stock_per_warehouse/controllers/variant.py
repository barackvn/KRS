# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import http
from odoo.http import request
from odoo.addons.sale.controllers.variant import VariantController

class VariantController(VariantController):
    @http.route()
    def get_combination_info(self, product_template_id, product_id, combination, add_qty, pricelist_id, **kw):
        values= super(VariantController, self).get_combination_info(
            product_template_id,
            product_id,
            combination,
            add_qty,
            pricelist_id,
            **kw
        )

        show_stocks = False
        show_qty    = False
        if product_template_id:
            template = request.env['product.template'].sudo().browse(product_template_id)
            website_config = request.env['warehouse.stock.config.settings'].sudo().search(
                [
                    ('website_id','=',request.website.id),
                    ('is_active','=',True),
                ],
            )
            if website_config:
                show_qty = website_config.show_qty
            if not website_config or website_config.user_visibility == 'product':
                if template.user_visibility == 'public':
                    show_stocks = True
                elif template.user_visibility == 'portal' and not request.website.is_public_user():
                    show_stocks = True
            else:
                if website_config.user_visibility == 'public':
                    show_stocks = True
                elif website_config.user_visibility == 'portal' and not request.website.is_public_user():
                    show_stocks = True

            if show_stocks and product_id:
                product = template.product_variant_ids.filtered(
                    lambda self: self.product_template_attribute_value_ids.ids == combination
                )
                warehouse_stocks = []
                if product.warehouse_stock_ids:
                    for warehouse_stock_id in product.warehouse_stock_ids:
                        warehouse_stock = {
                            'name': warehouse_stock_id.warehouse_id.name,
                            'qty' : warehouse_stock_id.virtual_available,
                        }
                        if website_config.qty_type == 'exclude_incoming_qty_available':
                            warehouse_stock['qty'] -= warehouse_stock_id.incoming_qty
                        warehouse_stocks.append(warehouse_stock)
                values['warehouse_stocks'] = warehouse_stocks

        values['show_stocks'] = show_stocks
        values['show_qty'] = show_qty
        return values
