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

class NewDeliveryOrderWizard(models.TransientModel):
    _inherit = 'new.delivery.order.wizard'

    @api.model
    def default_get(self, default_fields):
        res = super(NewDeliveryOrderWizard, self).default_get(default_fields)
        if rma_obj := self.env['rma.rma'].browse(self._context['active_id']):
            is_repaired = bool(rma_obj.mrp_repair_id)
            company_id = self.env.user.company_id.id
            picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing'), ('warehouse_id.company_id', '=', company_id)], limit=1)
            if not picking_type:
                picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing'), ('warehouse_id', '=', False)], limit=1)
            if not picking_type:
                raise ValidationError(_("Make sure you have at least an outgoing picking type defined"))
            source_location_id = None
            des_location_id = rma_obj.partner_id.property_stock_customer.id
            if is_repaired:
                if mrp_repair_id := self.env["repair.order"].browse(
                    int(rma_obj.mrp_repair_id)
                ):
                    source_location_id = mrp_repair_id.location_id.id
                    des_location_id = mrp_repair_id.location_dest_id.id

            elif rma_obj.return_request_type == 'exchange' and rma_obj.marketplace_seller_id:
                source_location_id = rma_obj.marketplace_seller_id.get_seller_global_fields('location_id')
                seller_warehouse_id = rma_obj.marketplace_seller_id.get_seller_global_fields('warehouse_id')
                picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing'), ('warehouse_id.company_id', '=', seller_warehouse_id)], limit=1)

            else:
                if picking_type.default_location_dest_id:
                    des_location_id = picking_type.default_location_dest_id.id
                if picking_type.default_location_src_id:
                    source_location_id = picking_type.default_location_src_id.id
            res.update({
                'rma_id': rma_obj.id,
                'source_location_id': source_location_id,
                'des_location_id': des_location_id,
                'picking_type_id': picking_type.id,
                'is_repaired': is_repaired,
                'product_id': rma_obj.product_id.id,
                'product_qty': rma_obj.refund_qty,
                'sale_order_id': rma_obj.order_id.id,
            })
            return res

    @api.onchange('picking_type_id')
    def onchange_picking_type_id(self):
        if self.rma_id.marketplace_seller_id and self.rma_id.return_request_type == 'exchange':
            picktype = self.env["stock.picking.type"].browse(self.picking_type_id.id)

            if picktype.default_location_dest_id:
                self.des_location_id = picktype.default_location_dest_id.id
            if picktype.default_location_src_id:
                self.source_location_id = self.rma_id.marketplace_seller_id.get_seller_global_fields('location_id')

        elif not self.is_repaired and self.picking_type_id:
            picktype = self.env["stock.picking.type"].browse(self.picking_type_id.id)
            if picktype.default_location_dest_id:
                self.des_location_id = picktype.default_location_dest_id.id
            if picktype.default_location_src_id:
                self.source_location_id = picktype.default_location_src_id.id
