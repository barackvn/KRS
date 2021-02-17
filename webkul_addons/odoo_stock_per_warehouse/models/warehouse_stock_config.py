# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import api,fields,models


class WarehouseStockConfigSettings(models.Model):
    _name = 'warehouse.stock.config.settings'
    _description = 'Warehouse Stock Configuration'


    name       = fields.Char('Name',required=True)
    is_active  = fields.Boolean('Active on website',default=False,copy=False)
    website_id = fields.Many2one(
        comodel_name = 'website',
        default      = lambda self:self.env.ref('website.default_website'),
        required     = True
    )
    qty_type = fields.Selection(
        string='Quantity Type',
        selection=[
            (
                'exclude_incoming_qty_available',
                'Onhand Quantity(Virtual Available-Incoming Quantity)'
            ),
            (
                'virtual_available',
                'Forcasted Quantity(Virtual Available)'
            ),
        ],
        default='virtual_available',
        required=True,
    )
    user_visibility = fields.Selection(
        selection=[
            ('hidden','Hidden'),
            ('product','Product Wise'),
            ('portal','Portal Users'),
            ('public','Public Users'),
        ],
        string='Stock Visibility',
        default='portal',
        required=True,
    )
    show_qty = fields.Boolean(
        string='Show Quantity',
        default=True,
    )

    @api.model
    def create(self, vals):
        if vals.get('is_active'):
            self.search(
                [
                    ('website_id','=',vals.get('website_id',self.env.ref('website.default_website').id)),
                    ('is_active','=',True),
                ]
            ).write({'is_active':False})
        return super(WarehouseStockConfigSettings, self).create(vals)

    def toggle_is_active(self):
        self.ensure_one()
        if not self.is_active:
            self.search(
                [
                    ('website_id','=',self.website_id.id),
                    ('is_active','=',True),
                ]
            ).write({'is_active':False})
        self.is_active = not self.is_active
