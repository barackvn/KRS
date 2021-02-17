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
  "name"                 :  "Odoo Maintenance Mode",
  "summary"              :  """Put your odoo website on maintenance mode in one click""",
  "category"             :  "Website",
  "version"              :  "3.0.0",
  "sequence"             :  45,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com",
  "description"          :  """https://store.webkul.com""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=odoo_maintenance_mode&version=12.0",
  "depends"              :  ['website'],
  "data"                 :  [
                             'views/maintenance_mode_view.xml',
                             'data/email_template.xml',
                             'views/res_config_view.xml',
                             'views/templates.xml',
                             'wizard/wizard_message_view.xml',
                             'security/ir.model.access.csv',
                             'data/demo.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  69,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}