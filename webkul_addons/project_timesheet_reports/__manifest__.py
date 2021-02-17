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
  "name"                 :  "Project Timesheet Reports",
  "summary"              :  "The module is used to print out the report of the timesheets in Odoo. The user can print the timesheet reports and send to another user via mail.",
  "category"             :  "Extra Tools",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Project-Timesheet-Reports.html",
  "description"          :  """Odoo Project Timesheet Reports
Print reports Odoo
Odoo reports
Timesheet report print""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=project_timesheet_reports&version=13.0",
  "depends"              :  [
                             'project',
                             'hr_timesheet',
                            ],
  "data"                 :  [
                             'report/task_report.xml',
                             'report/report_action.xml',
                             'data/mail_template.xml',
                             'views/wizard_view.xml',
                             'views/project_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  25,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}