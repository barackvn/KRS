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
  "name"                 :  "Advance Stock Inventory Import",
  "summary"              :  "The module allows you to update your stock of multiple products simultaneously in the Odoo through CSV/XLS file import.",
  "category"             :  "Marketing",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo.html",
  "description"          :  """The module allows you to update your stock of multiple products simultaneously in the Odoo through CSV/XLS file import.""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=advance_inventory_import",
  "depends"              :  [
                             'stock',
                            ],
  "data"                 :  [
                             'wizards/inventory_adjustment_view.xml',
                             'wizards/wizard_message_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  45,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
