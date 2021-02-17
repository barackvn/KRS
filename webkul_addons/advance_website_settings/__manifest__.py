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
  "name"                 :  "Website Cart Settings",
  "summary"              :  """This module provides additional features to your cart settings (like delete button, subtotal, minimum order, etc).""",
  "category"             :  "Website",
  "version"              :  "2.0.2",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Cart-Settings.html",
  "description"          :  """http://webkul.com/blog/website-cart-settings/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=advance_website_settings&version=13.0",
  "depends"              :  [
                             'website_sale',
                             'website_webkul_addons',
                            ],
  "data"                 :  [
                             'views/advance_website_settings_view.xml',
                             'views/webkul_addons_config_inherit_view.xml',
                             'views/template.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  29,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
