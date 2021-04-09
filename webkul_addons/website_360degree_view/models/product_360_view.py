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

from odoo import api, fields, models, tools, _
import logging
_logger = logging.getLogger(__name__)

class Product360View(models.Model):
    _name = 'product.360.view'
    _description = "Product Images For 360 Degree View"
    _order = 'sequence asc'

    name = fields.Char(string='Image Title',
                       help="A Title shows when you mouse over an image.")
    image = fields.Binary(string='Image', required=True)
    template_id = fields.Many2one(
        comodel_name='product.template', string='Product Template')
    sequence = fields.Integer(string='Sequence', required=True)

    @api.depends('image')
    def _compute_images(self):
        for rec in self:
            rec.image_small = tools.image_resize_image_small(rec.image)

    def _inverse_image_small(self):
        for rec in self:
            rec.image = tools.image_resize_image_big(rec.image_small)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.depends('template_360_images')
    def _get_number_of_images_for_360(self):
        for self_obj in self:
            if self_obj.template_360_images:
                self.number_of_images_for_360 = len(
                    self_obj.template_360_images)
            else:
                 self.number_of_images_for_360 = 0


    template_360_images = fields.One2many(
        comodel_name='product.360.view', inverse_name='template_id', string='Product 360 View Images')
    product_360_view = fields.Boolean(
        string="Show Product 360° View Only", help="Tick this field if you want to show product 360° view.")
    product_default_view = fields.Boolean(
        string="Show Product Default Image", help="Tick this field if you want to show product default(Odoo) view.",
        default= True)
    number_of_images_for_360 = fields.Integer(
        compute='_get_number_of_images_for_360', string="Number Of Images")

    @api.onchange('product_360_view')
    def on_change_product_360_view(self):
        if self.product_360_view:
            self.product_default_view = False

    @api.onchange('product_default_view')
    def on_change_product_default_view(self):
        if self.product_default_view:
            self.product_360_view = False

    def get_360_view_config(self):
        config_dict = self.env[
            "website.360.view.config"].get_default_product_360_view_fields()
        if config_dict.get("enable_360_view"):
            return config_dict["enable_360_view"]
        else:
            return False
