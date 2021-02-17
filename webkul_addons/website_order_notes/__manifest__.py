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
  "name"                 :  "Website Order Notes",
  "summary"              :  """Allow your Customers to leave a message/comment before placing an order.""",
  "category"             :  "Website",
  "version"              :  "3.0.3",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Internal-Notes-On-Order.html",
  "description"          :  """http://webkul.com/blog/odoo-website-notes-on-order/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_order_notes&version=13.0",
  "depends"              :  [
                             'sale_stock',
                             'website_webkul_addons',
                             'website_sale',
                            ],
  "data"                 :  [
                             'views/inherited_sale_order_views.xml',
                             'views/inherited_stock_picking_views.xml',
                             'views/inherited_account_invoice_views.xml',
                             'views/res_config_view.xml',
                             'views/templates.xml',
                             'views/webkul_addons_config_inherit_view.xml',
                            ],
  "demo"                 :  ['data/demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  25,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}