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
  "name"                 :  "Odoo GDPR",
  "summary"              :  """Make sure that your Odoo is in compliance with the GDPR! Give your users the right to manage their own data via portal login.""",
  "category"             :  "Extra Tools",
  "version"              :  "1.0.0",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "maintainer"           :  "Saurabh Gupta",
  "website"              :  "https://store.webkul.com/Odoo.html",
  "description"          :  """If you are running your website on Odoo, and looking for the GDPR Configuration website then you are at right place.""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=odoo_gdpr&version=12.0&custom_url=/my/home",
  "depends"              :  ['website_sale'],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/odoo_gdpr_view.xml',
                             'views/res_config_settings_views.xml',
                             'data/default_data.xml',
                             'views/odoo_gprd_portal_templates.xml',
                             'views/gdpr_data_template_view.xml',
                             'views/header_template.xml',
                             'views/address_template.xml',
                             'views/gdpr_request_view.xml',
                             'data/report_view.xml',
                            ],
  "demo"                 :  ['data/demo_data_view.xml'],
  "images"               :  ['static/description/banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  149,
  "currency"             :  "EUR",
}