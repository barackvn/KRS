# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    slider_min_price = fields.Integer(
        "Slider Min Price", config_parameter='theme_inventive.slider_min_price', default=0, required="True")
    slider_max_price = fields.Integer(
        "Slider Max Price", config_parameter='theme_inventive.slider_max_price', default=100000, required="True")
    price_range_step = fields.Integer(
        "Price Range Step",  config_parameter='theme_inventive.price_range_step', default=100, required="True")
    show_price_filter = fields.Boolean(
        "Show Price Filter", config_parameter='theme_inventive.show_price_filter')

    enable_lazy_loading = fields.Boolean('Enable Lazy Loading', default = False, config_parameter='theme_inventive.enable_lazy_loading')
    lazy_loading_options = fields.Selection([('button','Button Click'),('scroll',"On Scroll")], config_parameter = 'theme_inventive.lazy_loading_options', default = 'button')


    products_rating = fields.Selection(
        [('show', 'Show all the Ratings'),
            ('hide', 'Show Only that have value greater then 0'),
            ('hidden', 'Do not show Ratings at all.'),
         ],
        "Show/Hide Product Ratings", config_parameter='theme_inventive.products_rating', default="show")
    product_filter_views = fields.Selection([ ('default', 'Default'),('side_bar', 'Left Side bar'), ('dropdown', 'Dropdown')],
                                            "Product Filters Views", config_parameter='theme_inventive.product_filter_views', default="dropdown")

    product_quick_view = fields.Boolean(
        "Product Quick View", config_parameter='theme_inventive.product_quick_view')
    product_alternatives_view = fields.Boolean(
        "Product Alternates View", config_parameter='theme_inventive.product_alternatives_view')
    product_accessories_view = fields.Boolean(
        "Product Accessories View", config_parameter='theme_inventive.product_accessories_view')

    # Theme Preloader Configurations.......................................................................
    enable_preloader = fields.Boolean("Enable Website preloader", default=False, config_parameter="theme_inventive.enable_preloader")
    preloader_icon_class = fields.Selection([
        ('sk-dot',"Dot"),
        ('sk-rect','Rect'),
        ('sk-cube','Cube'),
        ('sk-bounce','Bounce'),
        ('sk-circle','Circle'),
        ('sk-cube-grid','Cube Grid'),
        ('sk-folding-cube','Folding Cube'),
        ('sk-fading-circle','Fading Circle'),
    ], "Icon",default="sk-cube-grid", config_parameter="theme_inventive.preloader_icon_class")
    use_preloader_image = fields.Boolean("Using Preloader Image", default=False, config_parameter="theme_inventive.use_preloader_image")
    preloader_image = fields.Binary(readonly=False, related='website_id.preloader')
    background_color = fields.Char("Background Color", default="#fff8dc", config_parameter="theme_inventive.background_color");
    background_opacity = fields.Selection([
        ('0','Opacity 0'),
        ('.2','Opacity 0.2'),
        ('.4','Opacity 0.4'),
        ('.6','Opacity 0.6'),
        ('.8','Opacity 0.8'),
        ('1','Opacity 1'),
    ],"Background Opacity",default=".8", config_parameter="theme_inventive.background_opacity");
    preloader_message =  fields.Char("Message", config_parameter="theme_inventive.preloader_message");
    preloader_text_color = fields.Char("Text Color", default="#daa520", config_parameter="theme_inventive.preloader_text_color")
    preloader_text_size = fields.Selection([
        ('16px',"16 Px"),
        ('20px','20 Px'),
        ('24px','24 Px'),
        ('28px','28 Px'),
        ('32px','32 Px'),
        ('36px','36 Px'),
        ('40px','40 Px'),
        ('44px','44 Px'),
    ], "Text Size", default="40px", config_parameter="theme_inventive.preloader_text_size")

    def set_values(self):
        super(ResConfigSettings, self).set_values()
