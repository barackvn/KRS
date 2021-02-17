# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import models, fields, api

class WarehouseStock(models.Model):
    _name = 'wk.warehouse.product.stock'
    _description = 'Warehouse Product Stock'

    def getAvailableQuantity(self):
        for rec in self:
            rec.qty_available = rec.product_id.with_context(
                warehouse=rec.warehouse_id.id
            ).qty_available

    def getVirtualQuantity(self):
        for rec in self:
            rec.virtual_available = rec.product_id.with_context(
                warehouse=rec.warehouse_id.id
            ).virtual_available

    def getIncomingQuantity(self):
        for rec in self:
            rec.incoming_qty = rec.product_id.with_context(
                warehouse=rec.warehouse_id.id
            ).incoming_qty

    def getOutgoingQuantity(self):
        for rec in self:
            rec.outgoing_qty = rec.product_id.with_context(
                warehouse=rec.warehouse_id.id
            ).outgoing_qty

    product_tmpl_id   = fields.Many2one('product.template')
    product_id        = fields.Many2one('product.product')
    warehouse_id      = fields.Many2one('stock.warehouse')
    qty_available     = fields.Float('Available Quantity',compute=getAvailableQuantity)
    virtual_available = fields.Float('Virtual Quantity',compute=getVirtualQuantity)
    incoming_qty      = fields.Float('Incoming Quantity',compute=getIncomingQuantity)
    outgoing_qty      = fields.Float('Outgoing Quantity',compute=getOutgoingQuantity)
