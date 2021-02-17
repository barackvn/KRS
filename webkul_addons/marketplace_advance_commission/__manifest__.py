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
  "name"                 :  "Odoo Marketplace Advance Commission",
  "summary"              :  "The admin can now set advanced commission rules for his/her Odoo Multi-vendor marketplace on products, products categories and sellers individually.",
  "version"              :  "1.0.2",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Marketplace-Advance-Commission.html",
  "description"          :  """Seller agent commission
Set seller commission
Admin commission on Odoo Marketplace
Marketplace seller commission
Commission rules
Odoo seller commission
Odoo Seller pays commission
Marketplace seller commission rules
New commission rules
Seller product commission
Product sale commission on marketplace
Odoo Marketplace
Odoo multi vendor Marketplace
Multi seller marketplace
Multi-seller marketplace
multi-vendor Marketplace
""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_advance_commission&lifetime=120&lout=1&custom_url=/",
  "depends"              :  ['odoo_marketplace'],
  "data"                 :  [
                             'data/mp_advance_comm_data.xml',
                             'views/res_partner_views.xml',
                             'views/mp_res_config_views.xml',
                             'views/inherit_website_categ.xml',
                             'views/inherit_mp_product_views.xml',
                             'views/inherit_seller_payment.xml',
                             'wizard/comm_type_info_wizard.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  99,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
