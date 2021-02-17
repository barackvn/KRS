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
  "name"                 :  "Website Order Cancel",
  "summary"              :  "The module allows the customers to cancel the website order quotation from their Odoo website account.",
  "category"             :  "Website",
  "version"              :  "1.0.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Order-Cancel.html",
  "description"          :  """Odoo Website Order Cancel
Cancel website order in Odoo
Odoo cancel customer quotation
Order Cancel button on Odoo website
Cancel order button in customer account
Cancel quotation button in customer account
Customer account quotation cancel button""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_order_cancel",
  "depends"              :  [
                             'sale_stock',
                             'website_webkul_addons',
                             'website_sale',
                             'sale'
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/inherited_sale_order_views.xml',
                             'views/cancellation_reason_view.xml',
                             'views/templates.xml',
                             'data/demo.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  39,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}