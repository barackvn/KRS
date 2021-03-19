# -*- coding: utf-8 -*-

{
  "name"                 :  "Custom ",
  "summary"              :  """The module allows you to display product information in separate tabs on the product page. Show product description. Technical details, etc. in tabs on website.""",
  "category"             :  "Website",
  "version"              :  "0.2.4",
  "sequence"             :  1,
  "author"               :  "Planet Odoo.",
  "depends"              :  ['snailmail','product','stock','base','odoo_marketplace','crm','stock', 'mp_advance_signup_customized', 'marketplace_rma'],
  "data"                 :  [
                             'data/ir_sequence_data.xml',
                             'data/cron.xml',
                             'security/ir.model.access.csv',
                             'views/mail_template_view.xml',
                             'views/res_partner_view.xml',
                             'views/product_view.xml',
                             'views/crm_lead_view.xml',
                             'views/pre_advise_view.xml',
                             # 'views/website_template_view.xml',
                            ],
  "demo"                 :  [],
  "images"               :  [],
  "application"          :  True,
  "installable"          :  True,
}
