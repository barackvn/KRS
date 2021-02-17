# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import models, fields, api, _

Tabs = [
    ('vertical','Vertical'),
    ('horizontal','Horizontal'),
]

class WkProductTabs(models.Model):
    _name = 'wk.product.tabs'
    _order = "sequence, name"
    _description = "Product Tab"
    active = fields.Boolean(
        default=1
    )
    sequence = fields.Integer(

    )
    name = fields.Char(
        required=1,
        translate= True
    )
    content = fields.Html(
        required=1,
        translate= True
    )
    tab_product_id  = fields.Many2one(
        comodel_name='product.template',
        string='Product'
    )

class Product(models.Model):
    _inherit = 'product.template'
    product_tab_type = fields.Selection(
        selection = Tabs,
        string= 'Tab Type',
        default='horizontal',
    )
    wk_product_tab_ids = fields.One2many(
        comodel_name='wk.product.tabs',
        inverse_name='tab_product_id',
        string='Product Tabs',
        domain=['|',('active','=',True),('active','=',False)],
    )
