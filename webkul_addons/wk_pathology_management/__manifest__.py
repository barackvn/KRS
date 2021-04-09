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
  "name"                 :  "Pathology Lab Management System",
  "summary"              :  """This module can be used in any Pathology Center to book any labtest and customer can get the report after the checkup.""",
  "version"              :  "1.0.0",
  "sequence"             :  0,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Pathology-Lab-Management-System.html",
  "description"          :  """https://webkul.com/blog/odoo-pathology-lab-management-system/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=wk_pathology_management&lifetime=60",
  "depends"              :  ['sale_management'],
  "data"                 :  [
                             'security/access_control_security.xml',
                             'security/ir.model.access.csv',
                             'report/patho_mgmt_report_template.xml',
                             'report/patho_mgmt_testreq_report_template.xml',
                             'edi/patho_reminder_mail_to_customer.xml',
                             'edi/mail_to_customer_on_approve_testrequest.xml',
                             'edi/send_report_by_email_to_customer.xml',
                             'views/patho_mgmt_menu_view.xml',
                             'views/patho_mgmt_patient_view.xml',
                             'views/patho_mgmt_config_view.xml',
                             'views/patho_mgmt_settings_view.xml',
                             'views/patho_mgmt_lab_test_view.xml',
                             'views/patho_mgmt_pathologist_view.xml',
                             'views/patho_mgmt_diagnosis_view.xml',
                             'views/patho_lab_test_unit.xml',
                             'views/patho_mgmt_test_parameters.xml',
                             'views/patho_testreq_view.xml',
                             'views/patho_mgmt_patho_source.xml',
                             'views/patho_lab_centers_view.xml',
                             'views/patho_lab_test_sample_type.xml',
                             'views/patho_lab_test_pre_info.xml',
                             'views/inherit_sale_views.xml',
                             'views/res_partner_view.xml',
                             'data/patho_mgmt_seq.xml',
                             'data/patho_mgmt_data.xml',
                             'data/patho_mgmt_config_data.xml',
                             'wizard/testreq_reject_reason_wizard_view.xml',
                             'wizard/patho_mgmt_diag_add_technician.xml',
                             'wizard/patho_mgmt_diag_obtval.xml',
                             'wizard/patho_user_wizard.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  99,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}