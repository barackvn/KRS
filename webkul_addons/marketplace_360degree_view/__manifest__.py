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
  "name"                 :  "Marketplace Product 360° View",
  "summary"              :  """Odoo Marketplace 360 Degree Product View facilitates Odoo Marketplace with the feature to show 360 Degree Product View""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  65,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Marketplace-Product-360-View.html",
  "description"          :  """Odoo Marketplace 360 Degree Product View
Marketplace 360 Degree Product View
Complete Product View
360 Degree Product View in Marketplace
360 Degree Product View
Product view
360 Degree View
Product View in Marketplace
View product
How to create 360° product photos for a Marketplace
360° product photos
Product photos
360° product view
Product images
360° product image view""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_360degree_view",
  "depends"              :  [
                             'odoo_marketplace',
                             'website_360degree_view',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'security/mp_360degree_security.xml',
                             'data/360degree_config_setting_data.xml',
                             'views/product_360_view.xml',
                             'views/res_config_view.xml',
                             'views/360degree_seller_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
