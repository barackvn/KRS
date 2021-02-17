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
  "name"                 :  "Odoo Website Customer Address Book",
  "summary"              :  "The module allows your Odoo website customers to add and save multiple billing and delivery address to their account, so they can use them in their orders.",
  "category"             :  "Website",
  "version"              :  "1.0.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Customer-Address-Book.html",
  "description"          :  """Odoo Website Customer Address Book
Add multiple delivery address for customer
Add multiple billing address
Add multiple shipping address
Save addresses in customer account
Choose different shipping and billing address""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_address_book",
  "depends"              :  ['website_sale'],
  "data"                 :  [
                             'views/address_book_template.xml',
                             'views/templates.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  45,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}