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
import datetime as a
from datetime import date
from datetime import datetime, timedelta
from odoo.tools.translate import _
from odoo import SUPERUSER_ID

import logging
_logger = logging.getLogger(__name__)


class SaleOrderline(models.Model):
    _inherit = "sale.order.line"

    @api.depends('move_ids')
    def _delivery_state(self):
        for line in self:
            if line.move_ids:
                line.delivery_state = all([proc.state in ['done'] for proc in line.move_ids])
            else:
                line.delivery_state = False


    @api.depends('move_ids')
    def _check_rma(self):
        for obj in self:
            rma_obj = self.env["rma.rma"].search(
                [('orderline_id', '=', obj.id)])
            if rma_obj:
                obj.rma_generated = True
            else:
                obj.rma_generated = False

    @api.model
    def _calculate_rma_qty(self):
        for obj in self:
            rma_obj = self.env["rma.rma"].search(
                [('orderline_id', '=', obj.id)])
            net_rma_qty = 0
            if rma_obj:
                for rma in rma_obj:
                    net_rma_qty += rma.refund_qty
                obj.net_rma_qty = net_rma_qty
            else:
                obj.net_rma_qty = 0

    def _check_eligibility_for_rma(self):
        config_setting = self.env["res.config.settings"].get_values()
        for obj in self:
            create_date = None
            if config_setting.get("days_for_rma", False):
                if config_setting.get("rma_day_apply_on", False) and config_setting["rma_day_apply_on"] == "so_date":
                    create_date = obj.create_date.date()
                if config_setting.get("rma_day_apply_on", False) and config_setting["rma_day_apply_on"] == "do_date":
                    move_line = self.env["stock.move"].search(
                        [("product_id", "=", obj.product_id.id), ("group_id.sale_id", "=", obj.order_id.name)])

                    if move_line and move_line[0].picking_id.date_done:
                        done_date = move_line[0].picking_id.date_done.date()
                        create_date = done_date
                days = timedelta(config_setting["days_for_rma"] or 0)
                today_date = datetime.today().date()
                if create_date:
                    valid_upto = create_date + days
                    if today_date <= valid_upto:
                        obj.is_eligible_for_rma = True
            else:
                obj.is_eligible_for_rma = False
            obj.is_eligible_for_rma = False if create_date == None else True

    delivery_state = fields.Boolean(
        compute="_delivery_state", string="Delivered", default=False)
    rma_generated = fields.Boolean(compute='_check_rma', string="RMA Created", default=False)
    net_rma_qty = fields.Float(
        compute='_calculate_rma_qty', string="RMA Qty")
    is_eligible_for_rma = fields.Boolean(
        compute="_check_eligibility_for_rma", string="Eligible For RMA", default=False)

    def rma_open_wizards_button(self):
        self.ensure_one()
        product_id_line = self.product_id
        partner_line = self.order_partner_id
        order_id_line = self.order_id
        order_qty = self.product_uom_qty
        rma_pool = self.env['rma.rma']
        rma_refund_qty = 0
        order_line_qty = self.product_uom_qty

        rma_search_ids = rma_pool.search([('partner_id', '=', partner_line.id), (
            'product_id', '=', product_id_line.id), ('order_id', '=', order_id_line.id)])
        for rma_obj in rma_search_ids:
            rma_state = rma_obj.state
            rma_no = rma_obj.name
            rma_refund_qty = rma_refund_qty + rma_obj.refund_qty
        if rma_refund_qty >= order_line_qty:
            text = 'Your RMA  Has Been Generated Already !!!'

            partial_id = self.env[
                'rma.message.successful'].create({'text': text})
            return {'name': "Message",
                    'view_mode': 'form',
                            'view_id': False,
                            'view_type': 'form',
                            'res_model': 'rma.message.successful',
                            'res_id': partial_id.id,
                            'type': 'ir.actions.act_window',
                            'nodestroy': True,
                            'target': 'new',
                    }

        else:
            vals = {
                'name': product_id_line.id,
                'wk_order_id': order_id_line.id,
                'qty_return': order_line_qty - rma_refund_qty,
                'partner_id': partner_line.id,
                'problem': ''
            }
            partial_id = self.env['rma.wizard'].create(vals)
            return {'name': "Message",
                    'view_mode': 'form',
                            'view_id': False,
                            'view_type': 'form',
                            'res_model': 'rma.wizard',
                            'res_id': partial_id.id,
                            'type': 'ir.actions.act_window',
                            'nodestroy': True,
                            'target': 'new',
                    }

    @api.model
    def get_rma_t_and_c(self):
        x = self.env["res.config.settings"].get_values(
        )["rma_term_condition"] or "No terms and policy"
        return x


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_rma_sale_setting(self):
        return self.env["res.config.settings"].get_values()
