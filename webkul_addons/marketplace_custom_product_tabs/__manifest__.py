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
  "name"                 :  "Odoo Marketplace Custom Product Tabs",
  "summary"              :  """Add product tabs on  product page to display additional content like product information, product details, technical specifications, warranty, etc.""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Marketplace-Custom-Product-Tabs.html",
  "description"          :  """Odoo Marketplace Custom Product Tabs
Product information tab
Website product details tab
Warranty information on website
Seller product information
Product extra details
Odoo Marketplace
Odoo multi vendor Marketplace
Multi seller marketplace
Multi-seller marketplace
multi-vendor Marketplace""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_custom_product_tabs&lifetime=120&lout=1&custom_url=/",
  "depends"              :  [
                             'odoo_marketplace',
                             'custom_product_tabs',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'security/marketplace_security.xml',
                             'views/product_views.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  10.0,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}