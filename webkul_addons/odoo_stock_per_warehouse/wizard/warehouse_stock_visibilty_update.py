# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import api,fields,models


class WarehouseStockVisibilityUpdate(models.TransientModel):
    _name = 'warehouse.stock.visibility.update'
    _description = 'Update Warehouse Stock Visibility'

    user_visibility = fields.Selection(
        selection=[
            ('hidden','Hidden'),
            ('portal','Portal Users'),
            ('public','Public Users'),
        ],
        string='Stock Visibility',
        default='hidden',
        required=True,
    )

    def update_visibility(self):
        self.env['product.template'].browse(
            self.env.context.get('active_ids')
        ).write({'user_visibility': self.user_visibility})
