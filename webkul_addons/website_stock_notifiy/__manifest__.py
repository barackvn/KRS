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
  "name"                 :  "Website Stock Notify",
  "summary"              :  """the module allows you to send e-mail notifications to your customers, when product is back in-stock.""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Stock-Notify.html",
  "description"          :  """Odoo Website Stock Notify
Email notifications
Send emails
Product in stock
Out of stock
Product alerts
Email alerts
Website email alerts
Product in stock alerts
Product in stock emails
Customer stock alerts""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_stock_notifiy",
  "depends"              :  [
                             'website_stock',
                             'mail',
                             'wk_wizard_messages',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'data/stock_notify_cron.xml',
                             'edi/website_notify_edi.xml',
                             'data/stock_action_server.xml',
                             'views/templates.xml',
                             'views/stock_notify_config_view.xml',
                             'views/website_stock_notification_view.xml',
                             'views/webkul_addons_config_inherit_view.xml',
                             'data/notify_config_demo.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  15,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}