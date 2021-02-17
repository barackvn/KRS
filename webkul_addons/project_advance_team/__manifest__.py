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
  "name"                 :  "Project Advance Team Management",
  "summary"              :  "The module allows you to create and manage teams in odoo. The user can assign team members and leader to the projects.",
  "category"             :  "Extra Tools",
  "version"              :  "1.0.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Project-Advance-Team-Management.html",
  "description"          :  """Odoo Project Advance Team Management
Manage team in Odoo
Assign team leader for projects in Odoo
Manage projects in Odoo
Add team members to the projects
Allow team manager in Odoo
Set teams for projects in Odoo""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=project_advance_team",
  "depends"              :  [
                             'project',
                             'hr',
                            ],
  "data"                 :  [
                             'security/project_security.xml',
                             'security/ir.model.access.csv',
                             'views/wk_team_view.xml',
                             'views/project_team_view.xml',
                            ],
  "demo"                 :  [
                             'data/data.xml',
                             'data/demo_data.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}