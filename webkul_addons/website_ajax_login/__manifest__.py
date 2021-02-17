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
  "name"                 :  "Website Ajax Login/Sign-Up",
  "summary"              :  """When the user clicks on Login/Sign-Up, the requested form appears in a very nice Ajax popup, integrated with facebook, odoo, google+.""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Login-Sign-Up.html",
  "description"          :  """http://webkul.com/blog/odoo-website-ajax-login-sign-up/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_ajax_login&lout=1&custom_url=/",
  "depends"              :  [
                             'website',
                             'auth_oauth',
                            ],
  "data"                 :  [
                             'data/website_ajax_config_demo.xml',
                             'view/ajax_login_template.xml',
                             'view/res_config.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  39,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}