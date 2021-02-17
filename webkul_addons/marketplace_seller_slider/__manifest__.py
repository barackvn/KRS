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
  "name"                 :  "Odoo Marketplace Seller Slider",
  "summary"              :  """The module allows your Odoo multi vendor marketplace sellers to add a slider on his seller shop page. The slider can display designs, products, etc to the customers.""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Marketplace-Seller-Slider.html",
  "description"          :  """Odoo Marketplace Seller Slider
Website slider
Product slider
Seller product slider on shop
Seller shop slider
Use sliders
Add product seller
Odoo Marketplace
Odoo multi vendor Marketplace
Multi seller marketplace
Multi-seller marketplace
multi-vendor Marketplace""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_seller_slider",
  "depends"              :  ['odoo_marketplace'],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/banner_image_view.xml',
                             'wizard/banner_images_wizard_view.xml',
                             'views/seller_or_shop_view.xml',
                             'views/seller_or_shop_template.xml',
                            ],
  "demo"                 :  [],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  25,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}