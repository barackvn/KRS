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
from datetime import date,datetime
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    test_date = fields.Date("Test Date", default=fields.Date.today())
    collection_center_id = fields.Many2one('patho.lab.centers', 'Collection Center',
        domain="[('is_collection_center','=', True)]",
        default = lambda self: self.env.user.partner_id.collection_center_id.id if self.env.user.partner_id.collection_center_id else self.env['ir.default'].get("res.config.settings", 'collection_center_id'))
    patho = fields.Boolean("Pathology")
    patho_testreq_id = fields.Many2one('patho.testrequest', string="Test Request")

    @api.onchange('order_line')
    def compute_patho(self):
        for rec in self:
            self.patho = False
            if rec.order_line:
                if any((line.product_id.is_test == True or line.product_id.is_test_package == True) for line in rec.order_line):
                    self.patho = True

    @api.onchange('test_date')
    def compute_testdate(self):
        if self.patho:
            if self.test_date:
                dt = self.test_date
                d1 = datetime.strptime(str(dt),"%Y-%m-%d").date()
                d2 = date.today()
                rd = relativedelta(d2,d1)
                if rd.days > 0 or rd.months > 0 or rd.years > 0:
                    raise UserError(_("Test Date Should be after Today"))

    def create_patho_testrequest(self):
        if not self.patho_testreq_id:
            testreq_vals = {
                'customer_id': self.partner_id.id,
                'test_date': self.test_date,
                'source': self.env.ref('wk_pathology_management.patho_source1').id,
                'sale_order_id': self.id,
                'collection_center_id': self.collection_center_id.id,
                'lab_center_id': self.collection_center_id.primary_labcenter_id.id,
                'status': 'pending',
                'description':self.note,
            }
            testreq_id = self.env['patho.testrequest'].create(testreq_vals)
            self.patho_testreq_id = testreq_id
            for line in self.order_line:
                if line.product_id.is_test or line.product_id.is_test_package:
                    patho_line = {
                        'testreq_id': testreq_id.id,
                        'name': line.name,
                        'product_id': line.product_id.id,
                        'product_qty': line.product_uom_qty,
                        'price_unit': line.price_unit,
                        'sale_order_line_id': line.id,
                        'discount': line.discount,
                    }
                    patho_line_id = self.env['patho.testrequest.lines'].create(patho_line)
        return


    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.patho:
            self.create_patho_testrequest()
        return res

    @api.model
    def create(self, vals):
        order = super(SaleOrder, self).create(vals)
        return order


    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if self.patho:
            self.compute_testdate()
            if self.order_line and self.patho_testreq_id and len(self.patho_testreq_id.patho_line_ids) != 0:
                for line in self.order_line:
                    if line.product_id.is_test or line.product_id.is_test_package:
                        if not any(patho_line.sale_order_line_id.id == line.id for patho_line in self.patho_testreq_id.patho_line_ids):
                            if self.patho_testreq_id.status == 'pending':
                                patholine = {
                                    'testreq_id': self.patho_testreq_id.id,
                                    'name': line.name,
                                    'product_id': line.product_id.id,
                                    'product_qty': line.product_uom_qty,
                                    'price_unit': line.price_unit,
                                    'sale_order_line_id': line.id,
                                }
                                patho_line_id = self.env['patho.testrequest.lines'].create(patholine)
                            else:
                                raise UserError(_("Test product cannot be added since the appointment has been already approved."))
        return res


    def action_invoice_create(self, grouped=False, final=False):
        res = super(SaleOrder, self).action_invoice_create(grouped, final)
        if self.patho:
            if len(self.patho_testreq_id.move_ids)== 0:
                self.patho_testreq_id.move_ids = [(6, 0, res)]
            else:
                self.patho_testreq_id.move_ids = [(4, res[0])]
            self.patho_testreq_id.invoice_count = len(set(self.move_ids.ids))
        return res
