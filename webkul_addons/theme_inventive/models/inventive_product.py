# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import models,fields,api

class InventiveProductTemplate(models.Model):
    _inherit = "product.template"

    def _compute_product_avg_rating(self):
        for product in self:
            total, rating = 0, 0.0
            for r in product.rating_ids:
                if r.rating:
                    rating += r.rating
                    total += 1
            product.total_start_rating_count = total
            product.product_avg_rating = rating/total if total and rating else 0.0

    sales_count             = fields.Float(compute='_compute_sales_count', string='Sold',store="True")
    product_avg_rating        = fields.Float("Product Average Rating", default=_compute_product_avg_rating ,readonly="True",store="True" )
    total_start_rating_count= fields.Integer("Total Start Rating Count")
