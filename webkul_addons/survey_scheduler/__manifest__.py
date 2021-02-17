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
  "name"                 :  "Scheduled Survey with Follow-Up",
  "summary"              :  "The module allows you to create survey and feedbacks can set time scheduler to send them to the customers. The users can schedule follow up mails.",
  "category"             :  "Marketing",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Scheduled-Survey-with-Follow-Up.html",
  "description"          :  """Odoo Scheduled Survey with Follow-Up
Send automatic surveys in Odoo
Create follow ups
Create feedback mail
Send feedback mail to customers
Schedule feedback mails in Odoo
Send survey mails to customers
Repeat follow up mails in Odoo""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=survey_scheduler",
  "depends"              :  ['survey'],
  "data"                 :  [
                             'security/survey_security.xml',
                             'security/ir.model.access.csv',
                             'data/cron.xml',
                             'views/survey_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  45,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}