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
  "name"                 :  "Financial Reports by Analytic Accounts",
  "summary"              :  "This module facilitates to print financial reports by Analytic Accounts",
  "category"             :  "Accounting",
  "version"              :  "1.0.2",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Financial-Reports-by-Analytic-Accounts.html",
  "description"          :  """This module facilates to print financial reports by Analytic Accounts.
  """,
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=account_analytic_reports",
  "depends"              :  ['accounting_pdf_reports'],
  "data"                 :  [
                             'views/common_report_excel.xml',
                             'views/financial_report.xml',
                             'data/data.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  25,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}