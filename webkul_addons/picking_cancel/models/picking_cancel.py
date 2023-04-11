# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models
from odoo.tools.float_utils import float_is_zero


class Picking(models.Model):
    _inherit = 'stock.picking'

    def action_cancel(self):
        for line in self.move_line_ids:
            self.env['stock.quant']._update_available_quantity(
                line.product_id,
                line.location_id,
                line.qty_done,
                lot_id=line.lot_id,
                package_id=line.package_id,
                owner_id=line.owner_id)
        self.mapped('move_lines')._action_cancel()
        self.write({'is_locked': True})
        return True


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def unlink(self):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        moves = self.mapped('move_id')
        for ml in self:
            # if ml.state in ('done', 'cancel'):
            #     raise UserError(_('You can not delete product moves if the picking is done. '
            #                       'You can only correct the done quantities.'))
            # Unlinking a move line should unreserve.
            if ml.product_id.type == 'product' and \
                not ml.location_id.should_bypass_reservation() and \
                    not float_is_zero(ml.product_qty, precision_digits=precision):
                self.env['stock.quant']._update_reserved_quantity(
                    ml.product_id,
                    ml.location_id,
                    -ml.product_qty,
                    lot_id=ml.lot_id,
                    package_id=ml.package_id,
                    owner_id=ml.owner_id,
                    strict=True)
        res = super(StockMoveLine, self).unlink()
        if moves:
            moves._recompute_state()
        return res


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _do_unreserve(self):
        for move in self:
            if move.state in ['done']:
                move.state = 'draft'
        # if any(move.state in ('cancel') for move in self):
        #     raise UserError(_('Cannot unreserve a done move'))
        self.mapped('move_line_ids').unlink()
        return True

    def _action_cancel(self):
        # if any(move.state == 'done' for move in self):
        #     raise UserError(_('You cannot cancel a stock move that has been set to \'Done\'.'))
        for move in self:
            if move.state == 'cancel':
                continue
            move._do_unreserve()
            siblings_states = (move.move_dest_ids.mapped('move_orig_ids') - move).mapped('state')
            if move.propagate_cancel:
                # only cancel the next move if all my siblings are also cancelled
                if all(state == 'cancel' for state in siblings_states):
                    move.move_dest_ids._action_cancel()
            elif all(state in ('done', 'cancel')
                       for state in siblings_states):
                move.move_dest_ids.write(
                    {'procure_method': 'make_to_stock'})
                move.move_dest_ids.write(
                    {'move_orig_ids': [(3, move.id, 0)]})
        self.write({'state': 'cancel', 'move_orig_ids': [(5, 0, 0)]})
        for line in self.mapped('sale_line_id'):
            line.qty_delivered = 0.0
        return True


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('move_ids', 'move_ids.state')
    def _compute_product_updatable(self):
        for line in self:
            if not line.move_ids.filtered(lambda m: m.state != 'cancel'):
                super(SaleOrderLine, line)._compute_product_updatable()
            else:
                line.product_updatable = False
