# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2019-Present Webkul Software Pvt. Ltd.
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
{
    "name"                 :    "Odoo Website Theme Inventive",
    "summary"              :    "Odoo Website Theme: Inventive offers an exquisite view and a better user experience for the visitors of your Odoo website.",
    "version"              :    "2.4.1",
    "sequence"             :    1,
    "author"               :    "Webkul Software Pvt. Ltd.",
    "license"              :    "Other proprietary",
    "website"              :    "https://store.webkul.com/catalogsearch/result/?cat=77&q=theme",
    "live_test_url"        :    "https://inventive_13.odoothemes.webkul.com/",
    "description"          :     """Inventive theme
                                    Webkul Odoo theme
                                    Odoo theme
                                    Website Theme
                                    themes in Odoo
                                    Odoo Website Theme: Inventive
                                    Theme Inventive in Odoo Website
                                    Odoo Website Theme Inventive
                                    Website Theme: Inventive
                                    Odoo Responsive theme
                                    Responsive theme
                                    theme
                                    themes
                                    Enhanced Theme
                                    website theme
                                    Best theme
                                    website outlook
                                    theme clarico
                                    Theme xtremo
                                    Inventive
                                    Theme Inventive
                                    Odoo""",

    "depends"               :   [
                                    "website_sale",
                                    "website_sale_wishlist",
                                    "website_blog",
                                    "website_sale_comparison",
                                    "website_sale_stock",
                                    "auth_oauth",
                                    "auth_signup",
                                    "mass_mailing",
                                    'sale',
                                ],
    "data"                 :    [
                                    'security/ir.model.access.csv',
                                    'views/inventive_assets_frontend.xml',
                                    "views/inventive_config_views.xml",
                                    "views/inventive_backend_views.xml",

                                    'views/theme_header_templates.xml',
                                    'views/theme_footer_templates.xml',
                                    'views/theme_shop_page_templates.xml',
                                    'views/inventive_lazy_load_templates.xml',
                                    'views/theme_login_pages_templates.xml',
                                    'views/theme_product_page_templates.xml',
                                    'views/theme_other_pages_templates.xml',
                                    'views/inventive_preloader_templates.xml',
                                    'views/product_tags_templates.xml',
                                    
                                    'views/inventive_common_snippets.xml',
                                    'views/inventive_common_snippet_options.xml',
                                    'views/inventive_mega_menu_snippets.xml',
                                ],
    "demo"                 :    [
                                    # 'data/demo_config.xml',
                                    # 'data/demo_public_categories.xml',
                                    # 'data/demo_products.xml',
                                ],
    "images"               :    [
                                    'static/description/Banner.png',
                                    'static/description/inventive_screenshot.gif'
                                ],

    "qweb"                 :  ['static/src/xml/*.xml'],
    "category"             : "Theme/Corporate",
    "installable"          :  True,
    "auto_install"         :  False,
    "price"                :  149,
    "currency"             :  "EUR",
}
