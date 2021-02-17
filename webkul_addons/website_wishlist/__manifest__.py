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
  "name"                 :  "Website Product Wishlist",
  "summary"              :  """Odoo Website Product Wishlist allows your customers to save their favourite products to the wishlist and shop them anytime by moving products to cart with just a single click.""",
  "category"             :  "Website",
  "version"              :  "1.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Product-Wishlist.html",
  "description"          :  """Odoo Website Product Wishlist
Product Wishlist
Product Wishlist in Odoo Website
Wishlist
Wishlist in Odoo Website
Manage Wishlist
Favourites
Wish Cart
Add to wishlist
Save For Later
Add to wishlist button
Heart like Icon wishlist""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_wishlist",
  "depends"              :  [
                             'website_sale',
                             'sale',
                             'sale_management',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/templates.xml',
                             'views/wk_wishlist.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  39,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}