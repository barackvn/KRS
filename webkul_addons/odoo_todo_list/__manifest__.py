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
  "name"                 :  "ODOO TODO List",
  "summary"              :  "The Odoo user can set up a 'ToDo' item note for any upcoming task or project. The Todo items do not appear in the tasks so they do not intervene with the current schedule.",
  "category"             :  "Project",
  "version"              :  "1.0.1",
  "sequence"             :  20,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-To-Do-List.html",
  "description"          :  """Odoo To Do List
ODOO TODO List
Add reminder to task
Add to-do list in odoo
Odoo project to-do list
Create To-Do item in odoo
""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=odoo_todo_list",
  "depends"              :  ['project'],
  "data"                 :  [
                             'views/views.xml',
                             'security/ir.model.access.csv',
                             'security/todo_security.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "EUR",
}