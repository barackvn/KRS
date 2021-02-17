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
  "name"                 :  "Project Task Start Stop",
  "summary"              :  "This module helps a user for managing timesheet on task.",
  "category"             :  "Project Management",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Project-Task-Start-Stop.html",
  "description"          :  """
Project Task Start Stop.
""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=project_start_stop&version=13.0",
  "depends"              :  [
                             'project',
                             'hr_timesheet'
                            ],
  "data"                 :  [
                             'wizard/work_log_wizard_view.xml',
                             'security/project_timesheet_security.xml',
                             'security/ir.model.access.csv',
                             'views/project_timesheet_view.xml',
                             'views/task_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "installable"          :  True,
  "application"          :  True,
  "auto_install"         :  False,
  "price"                :  25,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
