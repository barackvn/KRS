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
  "name"                 :  "Odoo Queue Management",
  "summary"              :  """Manage Queues in your store with Odoo queue Management module. Manage waiting lines with token system in your Odoo. the customer takes a token number and wait for their turn""",
  "category"             :  "Extra Tools",
  "version"              :  "1.0.2",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "website"              :  "https://store.webkul.com/Odoo-Queue-Management.html",
  "description"          :  """Odoo Queue management system
Queue management app
Queue management software
Waiting line
Queues
Work queue management
Booking queue management
Waiting queue management
Queue tokens
Taoken in queue
Token tickets
Token numbers
Appointment
scheduling
booking system""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=queue_management",
  "depends"              :  [
                             'mail',
                             'web_editor',
                             'website',
                            ],
  "data"                 :  [
                             'security/queue_management.xml',
                             'security/ir.model.access.csv',
                             'wizard/queue_message_wizard_view.xml',
                             'wizard/counter_department_view.xml',
                             'views/queue_management_template.xml',
                             'views/token_interface_templates.xml',
                             'views/queue_display_template.xml',
                             'views/queue_process_templates.xml',
                             'views/token_session_view.xml',
                             'views/token_interface_dashboard.xml',
                             'views/queue_process_view.xml',
                             'views/queue_counter_dashboard.xml',
                             'views/token_view.xml',
                             'views/department_view.xml',
                             'views/token_sequence_view.xml',
                             'views/queue_menus.xml',
                             'report/report_token_template.xml',
                             'report/token_report.xml',
                             'data/ir_sequence_data.xml',
                             'data/data.xml',
                            ],
  "demo"                 :  ['data/demo.xml'],
  "qweb"                 :  ['static/src/xml/queue_management_dashboard.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  149,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}