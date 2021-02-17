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
  "name"                 :  "Custom Products Tabs",
  "summary"              :  """The module allows you to display product information in separate tabs on the product page. Show product description. Technical details, etc. in tabs on website.""",
  "category"             :  "Website",
  "version"              :  "0.2.4",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "maintainer"           :  "Prakash Kumar",
  "website"              :  "https://store.webkul.com/Odoo-Custom-Product-Tabs.html",
  "description"          :  """Odoo Custom Product Tabs
                            Odoo Custom Products Tabs
                            Show product tabs on website
                            Website product tabs
                            Product page information tab in odoo
                            Website product information tabs
                            Product details tabs on product page
                            Odoo product technical details tab""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=custom_product_tabs",
  "depends"              :  ['website_sale'],
  "data"                 :  [
                             'views/template.xml',
                             'views/views.xml',
                             'security/ir.model.access.csv',
                            ],
  "demo"                 :  ['demo/demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  30.0,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}