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
    "name"  : "Odoo Marketplace Mass Upload",
    "summary"  :  """This module provides the facility to upload mass products and inventory""",
    "category" :  "Website",
    "version"  :  "1.0.0",
    "sequence" :  2,
    "author"   :  "Webkul Software Pvt. Ltd.",
    "license"  :  "Other proprietary",
    "website"  :  "https://store.webkul.com/Odoo-Marketplace-Mass-Upload.html",
    "description" :  """Odoo Marketplace Mass Upload
Odoo Marketplace Mass Upload Inventory
Mass Upload Inventory
Multiple Upload
Bulk upload
""",
  "live_test_url" :  "http://odoodemo.webkul.com/?module=marketplace_mass_upload",
  "depends"  :  [
                  'odoo_marketplace',
                ],
  "data"  :  [
                'security/ir.model.access.csv',
                'security/mass_upload_security.xml',
                'data/mass_upload_config_settings.xml',
                'data/mass_upload_settings_data.xml',
                'wizard/mass_upload_product_wizard.xml',
                'views/res_config_view.xml',
                'views/product_product_view.xml',
                'views/seller_view.xml',
                'views/mass_upload_product_view.xml',
                'views/mass_upload_inventory_view.xml',
                'views/mass_upload_settings.xml',
              ],
  "images" :  ['static/description/Banner.png'],
  "application"   :  True,
  "installable"   :  True,
  "auto_install"  :  False,
  "price"         :  99,
  "currency"      :  "EUR",
  "pre_init_hook" :  "pre_init_check",
}
