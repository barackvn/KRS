# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import models,api,tools,fields
import base64
import os
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
import math
import logging
_logger = logging.getLogger(__name__)

class WebsiteInherit(models.Model):
    _inherit = "website"

    preloader = fields.Binary("Website Preloader")
    def get_keep_reference(self):
        keep = QueryURL('/shop')
        return keep,slug

    def get_compute_currency_and_context(self):
        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])
        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)

        return [compute_currency, pricelist_context, pricelist]

    def get_rating_values(self,val):
        val_integer = math.floor(val)
        val_decimal = round(val - val_integer,3)
        if val_decimal> .75:
            val_integer +=1
            val_decimal = 0
        if val_decimal>=.25 and val_decimal<=.75:
            val_decimal = 0.5
        else:
            val_decimal = 0
        empty_star = 5 - (val_integer+math.ceil(val_decimal))
        return val_integer,val_decimal,empty_star


    def get_inventive_demo_products(self):
        return False
    # ........................FEATURED PRODUCT SNIPPET FUNCTIONS...............

    def get_inventive_new_products(self):
        domain = [('featured_product_type','=','new'),('tabs_product_type','=',False),('publish_status','=',True)]
        feature = self.env['inventive.features'].sudo().search(domain)
        return feature.products


    def get_inventive_featured_products(self):
        domain = [('featured_product_type','=','featured'),('tabs_product_type','=',False),('publish_status','=',True)]
        feature = self.env['inventive.features'].sudo().search(domain)
        return feature.products

    def get_inventive_rated_products(self):
        domain = [('featured_product_type','=','rated'),('tabs_product_type','=',False),('publish_status','=',True)]
        feature = self.env['inventive.features'].sudo().search(domain)
        return feature.products

    # ....................TAB PRODUCTS SNIPPET FUNCTIONS.........................

    def get_inventive_all_products(self):
        domain = [('tabs_product_type','=','all'),('publish_status','=',True)]
        feature = self.env['inventive.features'].sudo().search(domain)
        return feature.products


    def get_inventive_latest_products(self):
        domain = [('tabs_product_type','=','latest'),('publish_status','=',True)]
        feature = self.env['inventive.features'].sudo().search(domain)
        return feature.products

    def get_inventive_sale_products(self):
        domain = [('tabs_product_type','=','sale'),('publish_status','=',True)]
        feature = self.env['inventive.features'].sudo().search(domain)
        return feature.products





    def get_preloader_config(self):
        res_config = self.env['ir.config_parameter'].sudo()
        config = {}
        config["enable_preloader"] = res_config.get_param("theme_inventive.enable_preloader") or False
        config['preloader_icon_class'] = res_config.get_param("theme_inventive.preloader_icon_class") or "sk-bounce"
        config['use_preloader_image'] = res_config.get_param("theme_inventive.use_preloader_image") or False
        config['preloader_image'] = res_config.get_param("theme_inventive.preloader_image")
        config['background_color'] = res_config.get_param("theme_inventive.background_color")
        config['background_opacity'] = res_config.get_param("theme_inventive.background_opacity")
        config['preloader_message'] = res_config.get_param("theme_inventive.preloader_message")
        config['preloader_text_color'] = res_config.get_param("theme_inventive.preloader_text_color")
        config['preloader_text_size'] = res_config.get_param("theme_inventive.preloader_text_size")
        return config


    def get_active_product_tags(self):
        tags =self.env['th.product.tags'].search([('website_publish','=',True)])
        return tags.filtered(lambda tag : tag.product_ids)
