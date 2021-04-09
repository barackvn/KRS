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
  "name"                 :  "Odoo Marketplace Favourite Seller",
  "summary"              :  """With this module, the customers can set their favorite sellers in the Odoo marketplace. They can choose to follow their sellers and receive newsletters and updates about the products.""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  0,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Marketplace-Favourite-Seller.html",
  "description"          :  """Favorite seller list
Seller favorite
Follow seller
Follow marketplace seller
Favorite seller on Odoo
Saved sellers
Bookmark sellers marketplace
Bookmark marketplace sellers
Favorite store Odoo
Odoo Marketplace
Odoo multi vendor Marketplace
Multi seller marketplace
multi-vendor Marketplace""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_favourite_seller&lifetime=120&lout=1&custom_url=/",
  "depends"              :  ['odoo_marketplace'],
  "data"                 :  [
                             'security/access_control_security.xml',
                             'security/ir.model.access.csv',
                             'views/templates.xml',
                             'edi/notify_mail_to_followers.xml',
                             'views/mp_seller_followers.xml',
                             'views/mp_config_view.xml',
                             'views/mp_seller_view.xml',
                             'views/inherit_website_templates.xml',
                             'views/portal_account_favourite_seller_templates.xml',
                             'data/mp_favourite_seller_data.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  99,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}