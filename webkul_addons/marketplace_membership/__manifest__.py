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
  "name"                 :  "Odoo Marketplace Membership",
  "summary"              :  "Enroll seller into your Marketplace with Membership plans. The limit to the selling of products can be assigned to the seller according to the Odoo marketplace membership plans he/she purchases",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Marketplace-Membership.html",
  "description"          :  """Odoo Marketplace Membership
Online membership
Online membership system
Marketplace online membership portal
Website membership
Enroll seller
Seller membership
Odoo Marketplace
Odoo multi vendor Marketplace
Multi seller marketplace
Multi-seller marketplace
multi-vendor Marketplace
Website membership plans
Marketplace membership plans
""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_membership&lifetime=120&lout=0",
  "depends"              :  ['odoo_marketplace'],
  "data"                 :  [
                             'security/marketplace_security.xml',
                             'security/ir.model.access.csv',
                             'data/mp_config_setting_data.xml',
                             'wizard/mp_membership_wizard_views.xml',
                             'views/mp_membership_view.xml',
                             'views/product_views.xml',
                             'views/res_partner_views.xml',
                             'views/website_config_view.xml',
                             'views/marketplace_config_view.xml',
                             'views/website_template_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  149,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
