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
  "name"                 :  "Odoo Reminder Mail",
  "summary"              :  "With the Odoo Reminder module, you can send reminder emails to the Odoo users.Set the Odoo reminder and it is sent to the user email address on the scheduled date.",
  "category"             :  "Productivity",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/odoo-reminder-mail.html",
  "description"          :  """Send reminder mail
Odoo Reminder mail
Notify Odoo user with reminder mail
How to send reminders in Odoo
Send reminder mail notification
Reminder notifications
reminder alerts
Reminder mails to users
Set reminders in Odoo
Deliver notifications
Notifications in Odoo
Mail notifications for Odoo Users
Reminder Memos in Odoo
Configure deadline reminders in Odoo""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=odoo_reminder",
  "depends"              :  ['mail'],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'security/security.xml',
                             'data/cron.xml',
                             'views/reminder.xml',
                             'views/history.xml',
                             'templates/mail.xml',
                             'wizard/email_now.xml',
                            ],
  "demo"                 :  ['demo/reminder.reminder.csv'],
  "images"               :  ['static/description/banner.png'],
  "application"          :  True,
  "price"                :  45.0,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}