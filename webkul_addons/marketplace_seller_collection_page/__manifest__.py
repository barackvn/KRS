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
  "name"                 :  "Odoo Marketplace Seller Collection Page",
  "summary"              :  """The module provides a collection page to the Marketplace sellers so they can show their best collection of products to the customer on the Odoo marketplace""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  0,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Marketplace-Seller-Collection-Page.html",
  "description"          :  """Odoo Marketplace Seller Collection Page
Seller products
Website product carousels
Seller products collection
Group seller products
Marketplace seller collection
Online seller products
Seller best collection
Best products
Odoo Marketplace
Odoo multi vendor Marketplace
Multi seller marketplace
Multi-seller marketplace
multi-vendor Marketplace""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_seller_collection_page&lifetime=120&lout=1&custom_url=/collections",
  "depends"              :  [
                             'odoo_marketplace',
                             'website_collectional_page',
                            ],
  "data"                 :  [
                             'security/access_control_security.xml',
                             'security/ir.model.access.csv',
                             'views/mp_config_view.xml',
                             'views/mp_seller_view.xml',
                             'views/mp_collection_view.xml',
                             'views/mp_seller_profile_template.xml',
                             'data/mp_seller_collec_data.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}