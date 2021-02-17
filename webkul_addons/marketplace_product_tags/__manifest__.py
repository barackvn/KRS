# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
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
  "name"                 :  "Odoo Marketplace Product Tags",
  "summary"              :  "This module allows admin to manage tags and seller can use tags for their products, products will be filtered by these tags on website.",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "license"              :  "Other proprietary",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "website"              :  "https://store.webkul.com/Odoo-Multi-Vendor-Marketplace.html",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_product_tags&lifetime=120&lout=1&custom_url=/shop",
  "description"          :  """
  This module allows admin to manage tags and seller can use tags for their products, products will be filtered by these tags on website.
    Marketplace Product Tags
    Product Tags
    Marketplace Tags
    Search Product Using Tags
    Tags
    Tag Products
    """,
  "depends"              :  [
                             'odoo_marketplace',
                             'website_product_tags'
                            ],
  "data"                 :  [
                              'security/ir.model.access.csv',
                              'views/product_tags_view.xml',
                            ],
  "images"               : ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  10,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
