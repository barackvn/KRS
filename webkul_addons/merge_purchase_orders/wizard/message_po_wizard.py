# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import _, api, fields, models


class MessagePoWizard(models.TransientModel):
    _name = "message.po.wizard"
    _description = "Purchase order wizard message"

    text = fields.Text(string='Message', readonly=True, translate=True)

    def generated_message(self, message, name='Information'):
        partial = self.create({'text': message})
        return {
            'name': name,
            'view_mode': 'form',
            'res_model': 'message.po.wizard',
            'view_id': self.env.ref('merge_purchase_orders.message_po_wizard_form').id,
            'res_id': partial.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
        }
