# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import logging

from odoo import api, fields, models, _
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class StockWizardMessage(models.TransientModel):
    _name = "stock.inventory.wizard"
    _description = "Stock Inventory Wizard"

    text = fields.Text(string='Message')

    def generated_message(self, message, name='Message/Summary'):
        partial_id = self.create({'text': message}).id
        return {
            'name': name,
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'stock.inventory.wizard',
            'res_id': partial_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': self._context
        }

    def view_inventory(self):
        return {
            'name': 'Inventory',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'stock.inventory',
            'res_id': self._context.get('inventory_id'),
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            # 'target': 'new',
            'domain': '[]',
        }
