# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
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
    "name"                 :  "Odoo Marketplace Advertisement Manager",
    "summary"              :  "Sellers of marketplace can purchase an ad block and advertise their products.",
    "category"             :  "website",
    "version"              :  "1.0.0",
    "author"               :  "Webkul Software Pvt. Ltd.",
    "license"              :  "Other proprietary",
    "sequence"             :  0,
    "website"              :  "https://store.webkul.com/Odoo-Marketplace-Advertisement-Manager.html",
    "description"          :  """https://webkul.com/blog/odoo-marketplace-advertisement-manager/""",
    "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_advertisement_manager&version=13.0&lifetime=120&lout=1&custom_url=/advertisement",
    "depends"              :  [
        'odoo_marketplace',
        'website_advertisement_manager',
    ],
    "data"                 :  [
        "views/templates.xml",
        "views/inherit_ad_block_views.xml",
        "views/inherit_block_sol_views.xml",
        "views/inherit_website_templates.xml",
        "views/inherit_portal_account_ad_templates.xml",
        "data/mp_ad_block_data.xml",
    ],
    "images"               :  ['static/description/Banner.png'],
    "application"          :  True,
    "installable"          :  True,
    "auto_install"         :  False,
    "price"                :  99,
    "currency"             :  "EUR",
    "pre_init_hook"        :  "pre_init_check",
}
