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
  "name"                 :  "Website Daily Deals and Flash Sales",
  "summary"              :  """Provide daily deals or flashsales to your customers""",
  "category"             :  "Website",
  "version"              :  "3.2.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Daily-Deals.html",
  "description"          :  """http://webkul.com/blog/odoo-website-daily-deals/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_daily_deals&version=13.0&custom_url=/",
  "depends"              :  [
                             'website_sale',
                             'website_webkul_addons',
                             'stock',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'data/data.xml',
                             'view/website_daily_deals_view.xml',
                             'view/config_view.xml',
                             'view/webkul_addons_config_inherit_view.xml',
                             'view/templates.xml',
                            ],
  "demo"                 :  ['data/demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  99,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
