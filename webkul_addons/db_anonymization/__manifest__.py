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
  "name"                 :  "Database Anonymization",
  "summary"              :  """The module allows you to create dummy customers records in the Odoo to preserve privacy while sharing the database with third party.""",
  "category"             :  "Extra Tools",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "maintainer"           :  "Saurabh Gupta",
  "website"              :  "https://store.webkul.com/odoo-database-anonymization.html",
  "description"          :  """database backup
clone database
clone db
Odoo Database Anonymization
Conceal customer data Odoo
Create fake records In Odoo
Hide real contacts Odoo
Create dummy customer records in Odoo
Hide customer data in Odoo
Mask customer data""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=anonymization&lifetime=90&lout=1&custom_url=/",
  "depends"              :  [
                             'base',
                             'wk_wizard_messages',
                             'mail',
                            ],
  "data"                 :  [
                             'data/credential_mail_template.xml',
                             'data/default_data.xml',
                             'security/anonymization_access.xml',
                             'security/ir.model.access.csv',
                             'views/anonymize_query.xml',
                             'views/database_backup_view.xml',
                             'views/query_history.xml',
                             'views/faker_contact_view.xml',
                             'views/menues.xml',
                             'wizard/change_credential_view.xml',
                             'wizard/fake_contact_wizard_view.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "price"                :  99,
  "currency"             :  "EUR",
  "external_dependencies":  {'python': ['faker']},
}