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
  "name"                 :  "Google Tag Manager",
  "summary"              :  "The module integrates Odoo with Google Tag Manager so you can send the customer behaviour data from Odoo website to Google analytics.",
  "category"             :  "Website",
  "version"              :  "1.0.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Google-Tag-Manager.html",
  "description"          :  """Google Analytics
Floodlight
non-Google tags
Odoo Google Tag Manager
Odoo GTM
Integrate GTM with Odoo
Integrate Google Tag manager with Odoo
Use GTM in odoo
Track customer data
Google analytics in Odoo
Analyze website data
Track customer behaviour on website
    """,
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=odoo_google_tag_manager",
  "depends"              :  ['website_sale'],
  "data"                 :  [
                             'views/res_config_settings_views.xml',
                             'views/snippets_template.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "price"                :  45,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}