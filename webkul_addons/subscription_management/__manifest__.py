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
  "name"                 :  "Subscription Management",
  "summary"              :  "Subscription Management in Odoo facilitates the creation of subscription-based products in the Odoo.",
  "category"             :  "Sales",
  "version"              :  "1.4.4",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Subscription-Management.html",
  "description"          :  """Odoo Subscription Management
Subscription-based services in Odoo
Manage recurring bills in Odoo
Subscription management Software in Odoo
Subscription module for Odoo users
module for subscription management in Odoo
recurring billing management in Odoo
Subscription Module for Odoo
how to manage recurring services bills in Odoo
subscription services
subscription
Odoo subscription
manage subscription products in Odoo
Subscription products
Odoo Subscription Management
Odoo Website Subscription management
Odoo booking & reservation management
Odoo appointment management
Odoo website appointment management
""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=subscription_management",
  "depends"              :  [
                             'sale_management',
                             'product',
                            ],
  "data"                 :  [
                             'security/subscription_security.xml',
                             'security/ir.model.access.csv',
                             'views/inherit_product_view.xml',
                             'views/subscription_plan_view.xml',
                             'views/subscription_subscription_view.xml',
                             'views/subscription_sequence.xml',
                             'views/res_config_view.xml',
                             'wizard/cancel_reason_wizard_view.xml',
                             'wizard/message_wizard_view.xml',
                             'wizard/sale_order_line_wizard_view.xml',
                            #  'views/refund_invoice.xml',
                             'views/subscription_reason_view.xml',
                             'data/automatic_invoice.xml',
                            ],
"demo"                   : [ "data/subscription_management_data.xml", ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  69,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}