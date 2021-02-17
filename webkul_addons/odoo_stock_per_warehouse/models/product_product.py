# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import models, fields, api


class Product(models.Model):
    _inherit = 'product.product'

    def _getStockPerWarehouse(self):
        stock_warehouse_ids = self.env['stock.warehouse'].search(
            [('company_id','=',self.env.ref('base.main_company').id)]
        )
        for rec in self:
            self.env['wk.warehouse.product.stock'].search(
                [('product_tmpl_id','=',rec.product_tmpl_id.id)]
            ).sudo().unlink()
            for warehouse in stock_warehouse_ids:
                rec.warehouse_stock_ids+=self.env[
                    'wk.warehouse.product.stock'
                ].sudo().create(
                    {
                        'product_id'       : rec.id,
                        'warehouse_id'     : warehouse.id,
                        'product_tmpl_id'  : rec.product_tmpl_id.id,
                    }
                )

    warehouse_stock_ids = fields.One2many(
        comodel_name = 'wk.warehouse.product.stock',
        inverse_name = 'product_id',
        compute      = _getStockPerWarehouse
    )

