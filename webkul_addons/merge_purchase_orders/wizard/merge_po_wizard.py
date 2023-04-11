# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class MergePoWizard(models.TransientModel):
    _name = "merge.po.wizard"
    _description = "Merge purchase order wizard"

    partner_id = fields.Many2one('res.partner', string='Parnter')
    action_type = fields.Selection([
        ('merge_cancel', 'New Order and Cancel Selected'),
        ('merge_delete', 'New Order and Delete Selected'),
        ('merge_exist_cancel_other',
         'Merge on Selected Order and Cancel Others'),
        ('merge_exist_delete_other',
         'Merge on Selected Order and Delete Others'),
    ], default='merge_cancel', string='Action')

    select_order = fields.Many2one('purchase.order', 'Merge with')
    selected_orders = fields.Many2many('purchase.order', 'merge_po_wiz_id', 'merge_po_ids', 'merge_po_rel',
                                       domain=[('state', 'not in', ['purchase', 'done', 'cancel'])],
                                       string='Selected Orders')

    @api.onchange('partner_id')
    def onchange_partner(self):
        self.selected_orders = [(5, 0, 0)]
        if self.partner_id:
            domain = [
                ('partner_id', '=', self.partner_id.id),
                ('state', 'not in', ['purchase', 'done', 'cancel']),
            ]
            return {'domain': {'selected_orders': domain}}
        else:
            return {'domain': {'selected_orders': []}}

    @api.model
    def open_merge_wizard(self):
        ctx = dict(self._context or {})
        vals = {}
        if activeIds := ctx.get('active_ids'):
            vals['selected_orders'] = [(6, 0, activeIds)]
        partial = self.create(vals)
        return {
            'name': ("Merge PO"),
            'view_mode': 'form',
            'view_id': self.env.ref('merge_purchase_orders.merge_po_wizard_form').id,
            'res_model': 'merge.po.wizard',
            'res_id': partial.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'context': ctx,
            'domain': '[]',
        }

    def merge_purchase_orders(self):
        text = ''
        purchaseModel = self.env['purchase.order']
        if not (selectedOrdrs := self.selected_orders):
            raise ValidationError('Please add Purchase Orders to merge')
        state = selectedOrdrs.mapped('state')
        notDartt = ['purchase', 'done', 'cancel']

        if set(notDartt).intersection(state):
            raise ValidationError('All purchase order must be in Darft State!!!')
        parnterIds = selectedOrdrs.mapped('partner_id').ids
        if parnterIds.count(parnterIds[0]) != len(parnterIds):
            raise ValidationError('Partner/Vendor should be same for all PO!!!')
        if self.action_type in ['merge_exist_cancel_other', 'merge_exist_delete_other']:
            mergeWithPartnerId = self.select_order.partner_id.id
            if mergeWithPartnerId not in parnterIds:
                raise ValidationError('Partner/Vendor should be same for all PO and merging PO!!!')
            text = purchaseModel.merge_in_exist_order(selectedOrdrs, self.select_order, self.action_type)
        else:
            text = purchaseModel.merge_create_order(selectedOrdrs, self.action_type, parnterIds)
        return self.env['message.po.wizard'].generated_message(text)
