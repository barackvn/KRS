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
  "name"                 :  "Odoo Marketplace Ajax Login/Sign-Up",
  "summary"              :  """Odoo Marketplace Ajax Login/Sign-Up module allows you to provide access to anonymous users to register themselves on your marketplace.""",
  "category"             :  "Website",
  "version"              :  "1.0.1",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Marketplace-Ajax-Login-Sign-Up.html",
  "description"          :  """Odoo Marketplace Ajax Login/Sign-Up
Ajax login
Social login
Google sign in on Odoo
Facebook Sign In on Odoo website
Ajax Sign Up
Odoo Marketplace
Odoo multi vendor Marketplace
Multi seller marketplace
Multi-seller marketplace
multi-vendor Marketplace
One page sign in""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_ajax_login&lifetime=120",
  "depends"              :  [
                             'odoo_marketplace',
                             'website_ajax_login',
                            ],
  "data"                 :  ['view/mp_ajax_login_template.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  20,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}