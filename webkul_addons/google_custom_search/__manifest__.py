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
  "name"                 :  "Google Custom Search",
  "summary"              :  "The module allows you to integrate Google Search Engine with the Odoo website Search bar. Your website product results are shown using Google’s results.",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "website"              :  "https://store.webkul.com/Odoo-Google-Custom-Search.html",
  "description"          :  """Odoo Website Custom Search
Odoo Advanced Search Bar
Google Search Engine
Google Search Algo
Odoo Search with Google""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=google_custom_search",
  "depends"              :  ['website'],
  "data"                 :  [
                             'views/res_config_view.xml',
                             'views/template.xml',
                            ],
  "demo"                 :  ['demo/demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  69,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}