# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import models,api
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class ThemeInventive(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_inventive_post_copy(self, mod):
        self.disable_view('website_theme_install.customize_modal')

    @api.model
    def set_demo_config(self):
        try:
            products_add_to_cart    = request.env.ref('website_sale.products_add_to_cart').sudo()
            add_to_compare          = request.env.ref('website_sale_comparison.add_to_compare').sudo()
            products_categories     = request.env.ref('website_sale.products_categories').sudo()
            option_collapse_products_categories = request.env.ref('website_sale.option_collapse_products_categories').sudo()
            products_attributes     = request.env.ref('website_sale.products_attributes').sudo()
            products_description    = request.env.ref('website_sale.products_description').sudo()
            layout_logo_show        = request.env.ref('website.layout_logo_show').sudo()
            affix_top_menu          = request.env.ref('website.affix_top_menu').sudo()
            product_picture_magnify = request.env.ref('website_sale.product_picture_magnify').sudo()
            product_picture_magnify_auto = request.env.ref('website_sale.product_picture_magnify_auto').sudo()
            list_view = request.env.ref('website_sale.products_list_view').sudo()
        except Exception as e:
            _logger.info("\n............................Exception in demo data setting............%r.....................................",str(e))

        if products_add_to_cart:  products_add_to_cart.active = True
        if add_to_compare:   add_to_compare.active = True
        if products_categories: products_categories.active=True
        if products_attributes: products_attributes.active = True
        if products_description: products_description.active = True
        if layout_logo_show: layout_logo_show.customize_show = False
        if product_picture_magnify:  product_picture_magnify.active = True
        if product_picture_magnify_auto:  product_picture_magnify_auto.active = True

        if affix_top_menu:
            affix_top_menu.active = True
            affix_top_menu.customize_show = True
        if list_view:
            list_view.active = True
            list_view.customize_show = False
        if option_collapse_products_categories:
            option_collapse_products_categories.active = False
            option_collapse_products_categories.customize_show = False

        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('auth_signup.invitation_scope', "b2c")
        set_param('auth_signup.reset_password', True)
        set_param('auth_oauth.module_auth_oauth', True)
        set_param('theme_inventive.product_quick_view', True)
        set_param('theme_inventive.product_alternatives_view', True)
        set_param('theme_inventive.product_accessories_view', True)
        set_param('theme_inventive.product_filter_views', 'dropdown')
        set_param('theme_inventive.products_lazy_load', True)
        set_param('theme_inventive.show_price_filter', True)

        self.env["auth.oauth.provider"].browse(self.env.ref('auth_oauth.provider_openerp').id).enabled = True
        self.env["auth.oauth.provider"].browse(self.env.ref('auth_oauth.provider_facebook').id).enabled = True
        self.env["auth.oauth.provider"].browse(self.env.ref('auth_oauth.provider_google').id).enabled = True
        self.env["payment.acquirer"].browse(self.env.ref('payment.payment_acquirer_stripe').id).website_published = True
        return True
