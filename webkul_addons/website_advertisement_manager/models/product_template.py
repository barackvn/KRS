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
from odoo.exceptions import UserError
from datetime import date,datetime,timedelta
import logging
_logger = logging.getLogger(__name__)

BLOCK_POS = [
    # ("home_page_full_top", "Display At Home"),
    ("shop_page_full_top", "Top Container in Shop Page"),
    ("shop_page_full_bottom", "Bottom Container in Shop Page"),
    ("below_product_categories", "Side Div Below Products Category"),
    ("product_image_bottom", "Container Below Product Details in Product Page"),
    # ("cart_left", "Left Side Div in Cart Page"),
    # ("cart_right", "Right Side Div in Cart Page"),
    ("cart_full_bottom", "Bottom Container in Cart Page"),
    # ("checkout_page_left_side", "Left Side Div in Checkout Page"),
    # ("checkout_page_right_side", "Right Side Div in Checkout Page"),
    # ("payment_page_left_side", "Left Side Div in Payment Page"),
    # ("payment_page_right_side", "Right Side Div in Payment Page"),
    # ("checkout_full_bottom", "Bottom Container in Checkout Page"),
    ("payment_full_bottom", "Bottom Container in Payment Page"),
    # ("confirmation_page_right_bottom", "Side Div in Right Bottom in Confirmation Page"),
    ("confirmation_page_full_bottom", "Bottom Container in Confirmation Page"),
]

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_ad_block = fields.Boolean("Is Ad Block")
    block_position = fields.Selection(BLOCK_POS, string="Ad Block Position")
    ad_block_state = fields.Selection([
        ("available", "Available"),
        ("not_available", "Not Available"),
    ], string="State", default="available", track_visibility='onchange', compute="compute_ad_block_sol_status")
    allow_external_link = fields.Boolean(string="Allow External Link",
        help="Enable to allow external links on this block."
    )
    ad_block_sol_id = fields.Many2one("sale.order.line", compute="compute_ad_block_sol_status")
    ad_current_customer = fields.Char("res.partner", related="ad_block_sol_id.order_partner_id.name")
    ad_block_image = fields.Binary("Ad Block Image")
    ad_block_sol_ids = fields.One2many("sale.order.line", "ad_block_product_tmpl_id", "Ad Block Lines", copy=True, auto_join= True)

    _sql_constraints = [
        ('unique_block_position', 'unique(block_position)',
        _('There is already a record with this block position.'))
    ]

    def compute_ad_block_sol_status(self):
        for record in self:
            record.ad_block_sol_id = False
            record.ad_block_state = 'available'

            obj1 = self.env['sale.order.line'].search([
                ('is_ad_block_line','=', True),
                ('ad_block_status','!=','expire'),
                ('state','=','sale'),
                ('product_id', '=', record.product_variant_id.id)
            ])
            if obj1:
                date_today = date.today()
                for rec in obj1:
                    ad_expire_day = datetime.strptime(str(rec.ad_date_to),"%Y-%m-%d").date() + timedelta(days=1)
                    ad_date_from = datetime.strptime(str(rec.ad_date_from),"%Y-%m-%d").date()
                    ad_date_to = datetime.strptime(str(rec.ad_date_to),"%Y-%m-%d").date()
                    if date_today >= ad_expire_day:
                        record.ad_block_sol_id = False
                        record.ad_block_state = 'available'                        

            obj2 = self.env['sale.order.line'].search([
                ('is_ad_block_line','=', True),
                ('ad_block_status','!=','expire'),
                ('state','=','sale'),
                ('product_id', '=', record.product_variant_id.ids)
            ])
            if obj2:
                date_today = date.today()
                for rec in obj2:
                    ad_date_from = datetime.strptime(str(rec.ad_date_from),"%Y-%m-%d").date()
                    ad_date_to = datetime.strptime(str(rec.ad_date_to),"%Y-%m-%d").date()
                    if date_today == ad_date_from or date_today == ad_date_to:
                        record.ad_block_sol_id = rec.id
                        record.ad_block_state = 'not_available'

        return True

    def toggle_website_published(self):
        for record in self:
            record.sudo().website_published = not record.sudo().website_published

    def _check_block_price(self, vals):
        price = vals.get('lst_price') if vals.get('lst_price') else self.lst_price
        if price and price <= 0.0:
            raise UserError(_("Price of block must be greater than 0."))

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        res._check_block_price(vals)
        return res

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if vals.get('lst_price'):
            self._check_block_price(vals)
        return res
