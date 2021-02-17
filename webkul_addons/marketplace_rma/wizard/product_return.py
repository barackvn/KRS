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
from odoo.exceptions import except_orm, Warning, RedirectWarning, ValidationError
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
import datetime
import logging
_logger = logging.getLogger(__name__)


class ProductReturnWizard(models.TransientModel):
    _inherit = 'product.return.wizard'

    @api.model
    def _get_picking_in(self):
        company_id = self.env['res.users'].browse(self._uid).company_id.id
        rma_obj = self.env['rma.rma'].browse([self._get_rma()])
        marketplace_seller_obj = rma_obj.marketplace_seller_id

        if rma_obj and rma_obj.return_request_type in ('exchange','refund') and marketplace_seller_obj:
            
            seller_warehouse_id = marketplace_seller_obj.get_seller_global_fields('warehouse_id')
            types = self.env['stock.picking.type'].search([('code', '=', 'incoming'), ('warehouse_id', '=', seller_warehouse_id)])
        else:
            types = self.env['stock.picking.type'].search(
                [('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)])
        
        if not types:
            types = self.env['stock.picking.type'].search(
                [('code', '=', 'incoming'), ('warehouse_id', '=', False)])
            if not types:
                raise ValidationError(_("Make sure you have at least an incoming picking type defined"))
        return types[0]

    picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type',
                                      help="This will determine picking type of incoming shipment", required=True, default= _get_picking_in)
    marketplace_seller_id = fields.Many2one('res.partner', string="Seller", related="product_id.marketplace_seller_id")
    
    @api.onchange('picking_type_id')
    def onchange_picking_type_id(self):

        marketplace_seller_obj = self.rma_id.marketplace_seller_id
        des_location_id = None

        if self.rma_id and self.rma_id.return_request_type == 'repair':
            repair_location_id = self.env['ir.default'].sudo().get('res.config.settings', 'repair_location_id')
            if repair_location_id:
                des_location_id = repair_location_id

        elif self.rma_id and self.rma_id.return_request_type in ('exchange','refund') and marketplace_seller_obj:
            exchange_location_id = marketplace_seller_obj.get_seller_global_fields('location_id')

            if exchange_location_id:
                des_location_id = exchange_location_id
        elif self.picking_type_id:
            picktype = self.env["stock.picking.type"].browse(
                self.picking_type_id.id)
            if picktype.default_location_dest_id:
                des_location_id = picktype.default_location_dest_id.id
        
        self.des_location_id = des_location_id

    def apply(self):
        self.ensure_one()
        # Create new picking for returned products
        pick_type_id = self.picking_type_id.id
        new_picking = self.env["stock.picking"].create({
            'move_lines': [],
            'picking_type_id': pick_type_id,
            'state': 'draft',
            'origin': self.rma_id.name,
            'partner_id': self.rma_id.partner_id.id,
            'priority': self.priority,
            'location_id': self.source_location_id.id,
            'location_dest_id': self.des_location_id.id,
            'group_id': self.rma_id.order_id.procurement_group_id.id,
            'marketplace_seller_id': self.marketplace_seller_id.id
        })
        
        x = self.env["stock.move"].create({
            'product_id': self.product_id.id,
            'product_uom_qty': float(self.product_qty),
            'name': self.product_id.partner_ref,
            'product_uom': self.product_id.uom_id.id,
            'picking_id': new_picking.id,
            'state': 'draft',
            'origin': self.rma_id.name,
            'location_id': self.source_location_id.id,
            'location_dest_id': self.des_location_id.id,
            'picking_type_id': pick_type_id,
            'warehouse_id': self.picking_type_id.warehouse_id.id,
            'procure_method': 'make_to_stock',
            'group_id': self.rma_id.order_id.procurement_group_id.id,
        })
        new_picking.action_confirm()
        new_picking.action_assign()

        new_picking.sale_id = self.sale_order_id.id
        self.env["rma.rma"].browse(self.rma_id.id).write(
            {"picking_id": new_picking.id})
        
        return new_picking, pick_type_id