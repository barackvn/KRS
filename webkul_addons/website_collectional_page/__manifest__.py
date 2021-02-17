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
  "name"                 :  "Website Collection Page",
  "summary"              :  """The module allows you to create a product collection page on the Odoo website. Combine and display products on the basis of different collections""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Collection-Page.html",
  "description"          :  """Odoo Website Collection Page
Website product carousels
Odoo products collection
Group products
Combine product collection
website product collection
best collection
Best products""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_collectional_page&lifetime=60&lout=0&custom_url=/collections",
  "depends"              :  [
                             'website_sale',
                             'website_webkul_addons',
                             'sale_management',
                            ],
  "data"                 :  [
                             'security/collectional_security_view.xml',
                             'security/ir.model.access.csv',
                             'view/website_collectional_page.xml',
                             'view/templates.xml',
                             'data/wk_operator.xml',
                             'view/website_collectional_page_config.xml',
                             'view/webkul_addons_config_views.xml',
                             'view/collections_page_n_group_template.xml',
                            ],
  "demo"                 :  ['demo/wk_collection_demo_data.xml'],
  "css"                  :  ['static/src/css/collection.css'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  69,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}