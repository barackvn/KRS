# -*- coding: utf-8 -*-
#################################################################################
#
#	Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################
from odoo import api, fields , models

class website(models.Model):
	_inherit = 'website'

	def get_wk_brands(self,brand_set):
		return self.env['wk.product.brand'].sudo().browse(list(set(brand_set)))

	def get_filter_brand(self,wk_brands):
		filter_brand=''
		for wk_brand in wk_brands:
			filter_brand+='%s,'%(wk_brand.id)
		return filter_brand
		return ','.join(map(str,wk_brands.ids))

class product_template(models.Model):
	_inherit = 'product.template'

	product_brand_id = fields.Many2one(
		string='Brand',
		comodel_name="wk.product.brand"
	)

class Wk_ProductBrand(models.Model):
	_name = "wk.product.brand"
	_inherit = ['website.published.mixin']
	_description = "Website Product Brand"

	@api.depends('products')
	def _get_product_count(self):
		self.total_products = len(self.products.ids)

	name = fields.Char(
		string="Brand Name",required=True,
		translate=True
	)
	image = fields.Binary(
		string='product  image',
		help = " This Image will be visible to user in there shop  by brand onwebsite view !"
	)
	description = fields.Text(
		string ="Brand Description",
		translate=True
	)
	sequence = fields.Integer(
		string = "Sequence" ,
		help = "Gives the sequence order when displaying a list of brand onwebsite view.!"
	)
	products = fields.One2many(
		'product.template',
		'product_brand_id',
	)
	total_products = fields.Integer(
		string="Total no. of Products",
		compute=_get_product_count,
		store=True
	)

	@api.model
	def wk_activate_website_view(self):
		products_description = self.env.ref('website_sale.products_description')
		products_attributes = self.env.ref('website_sale.products_attributes')
		products_description.write(dict(active=1))
		products_attributes.write(dict(active=1))
		return True
