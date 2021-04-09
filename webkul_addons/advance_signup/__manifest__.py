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
    "name" : "Odoo Advance Signup",
    "summary" : "Odoo admin can configure their signup page with dynamic fields for each website.",
    "category" : "website",
    "sequence" : 1,
    "version" : "1.2.1",
    "author" : "Webkul Software Pvt. Ltd.",
    "license" : "Other proprietary",
    "website" : "https://store.webkul.com/",
    "description"          :  """Odoo Advance Sign Up
Advance Sign Up in Odoo
Sign Up Page
Advance Sign Up page
Advance Sign Up
Enhanced Sign Up page
Extra Information Sign Up
Log in Page
Password Reset Page
Reset Log in password
""",
    "live_test_url" : "http://odoodemo.webkul.com/?module=advance_signup&custom_url=/web/login&lout=1",
    "depends" : [
        'auth_signup','website',
    ],
    "data" : [
        "security/ir.model.access.csv",
        "views/templates.xml",
        "views/auth_signup_login_templates.xml",
        "wizard/field_add_domain.xml",
        "views/advance_signup_views.xml",
        "data/adv_signup_data.xml",
    ],
    "demo" : [
    ],
    "images" : [
        'static/description/Banner.png'
    ],
    "application" : True,
    "installable" : True,
    "auto_install" : False,
    "price" : 59,
    "currency" : "EUR",
    "pre_init_hook" : "pre_init_check",
}
