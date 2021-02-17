# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import models, fields, api


class Product(models.Model):
    _inherit = 'product.template'

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

    warehouse_stock_ids = fields.One2many(
        comodel_name = 'wk.warehouse.product.stock',
        inverse_name = 'product_tmpl_id',
    )
