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
  "name"                 :  "Pathology Digital Signature",
  "summary"              :  """The module allows you upload a digital signature and use it on the pathology lab reports. You can print the reports with a signature automatically added to it.""",
  "category"             :  "Extra Tools",
  "version"              :  "1.0.0",
  "sequence"             :  0,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Pathology-Digital-Signature.html",
  "description"          :  """Odoo Pathology Digital Signature
Add signature in reports
Use digital signature in reports
Upload signature in Odoo reports
Display signature in reports
Digital sign in Odoo
Add digital signature
Print signature in Odoo reports""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=pathology_digital_signature",
  "depends"              :  ['wk_pathology_management'],
  "data"                 :  [
                             'views/inherit_pathologist_view.xml',
                             'views/inherit_patho_lab_center_view.xml',
                             'views/inherit_patho_report_template.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  10,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}