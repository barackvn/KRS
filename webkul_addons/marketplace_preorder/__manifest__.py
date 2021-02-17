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
  "name"                 :  "Odoo Marketplace Pre-Order",
  "summary"              :  "The module allows the admin to take back-orders and pre-orders in the odoo Marketplace.",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  11,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Marketplace-Pre-Order.html",
  "description"          :  """Accept pre-order
Marketplace product pre-orders
Back orders
Backorders
Pre-order marketing
Odoo marketplace pre-order
Odoo pre-sales
Pre-order campaign
Pre-order sale
Odoo Marketplace
Odoo multi vendor Marketplace
Multi seller marketplace
Multi-seller marketplace
multi-vendor Marketplace
Out of stock orders
""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_preorder&lifetime=120&lout=1&custom_url=/",
  "depends"              :  [
                             'odoo_marketplace',
                             'website_preorder',
                            ],
  "data"                 :  [
                             'data/mp_preorder_data.xml',
                             'views/res_config_view.xml',
                             'views/seller_dashboard_product_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  25,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}