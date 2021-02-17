#  -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################
{
  "name"                 :  "Module For Merging Pos/Website Coupons",
  "summary"              :  "Module for merging POS/Website Coupons",
  "category"             :  "Hidden",
  "version"              :  "6.0.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo.html",
  "description"          :  """""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=wk_coupons&version=13.0",
  "depends"              :  [
                             'sale',
                             'mail',
                            ],
  "data"                 :  [
                            
                             'views/wk_coupon_view.xml',
                             'views/coupon_history_view.xml',
                             'report/report.xml',
                             'report/report_template.xml',
                             'security/ir.model.access.csv',
                             'data/coupon_data_view.xml',
                             'data/mail_template.xml',
                             'views/res_config_view.xml',
                             'wizard/wizard_view.xml',
                            ],
  "demo"                 :  ["data/demo.xml"],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  1,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}