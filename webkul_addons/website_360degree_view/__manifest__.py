# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
  "name"                 :  "Website Product 360 View",
  "summary"              :  """Odoo Website 360 Degree Product View facilitates Odoo Website with the feature to show 360 Degree Product View""",
  "category"             :  "Website",
  "version"              :  "2.0.1",
  "sequence"             :  65,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-360-Product-View.html",
  "description"          :  """Odoo Website 360 Degree Product View
Website 360 Degree Product View
Complete Product View
360 Degree Product View in website
360 Degree Product View
Product view
360 Degree View
Product View in Website
View product
How to create 360° product photos for a website
360° product photos
Product photos
360° product view
Product images
360° product image view""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_360degree_view&",
  "depends"              :  [
                             'sale_management',
                             'website_sale',
                             'website_webkul_addons',
                            ],
  "data"                 :  [
                             'view/product_360_view.xml',
                             'view/templates.xml',
                             'view/res_config_view.xml',
                             'view/webkul_addons_config_inherit_view.xml',
                             'security/ir.model.access.csv',
                             'data/product_360_data.xml',
                            ],
  "demo"                 :  ['demo/product_360_demo_data.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  76,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}