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
  "name"                 :  "Odoo Marketplace Seller Story",
  "summary"              :  """Post seller comments and stories on your Odoo multi vendor marketplace. Build social audience with sellers stories""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  10,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Marketplace-Seller-Story.html",
  "description"          :  """Odoo Marketplace Seller Story
publish seller story
post stories on website
website stories
customer stories
testimonials
Marketplace seller stories
seller experience
social tabs
social netwrok
Seller social
Odoo Marketplace
Odoo multi vendor Marketplace
Multi seller marketplace
Multi-seller marketplace
multi-vendor Marketplace
Marketplace Seller stories""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_seller_story",
  "depends"              :  ['odoo_marketplace'],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/mp_seller_story_view.xml',
                             'views/res_partner_views.xml',
                             'views/marketplace_template_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  99,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}