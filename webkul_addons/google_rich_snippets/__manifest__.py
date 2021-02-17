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
  "name"                 :  "Google Rich Snippets",
  "summary"              :  "Odoo Google Rich Snippets module lets you enable rich results on Google SERPs for your Odoo website.",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Google-Rich-Snippets.html",
  "description"          :  """Structured Data Markup
Odoo Google Rich Snippets
Google Rich Snippets in Odoo 
Google Rich Snippets 
Rich Snippets 
Snippets
rich cards
enriched results
Google enriched results
0th Position
Rich Results
Schema Markup
Google Search Results
Google Search
Serps""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=google_rich_snippets",
  "depends"              :  [
                             'website_sale_stock',
                             'website_webkul_addons',
                            ],
  "data"                 :  [
                             'views/snippets_template.xml',
                             'views/res_config_settings_views.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "price"                :  45,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}