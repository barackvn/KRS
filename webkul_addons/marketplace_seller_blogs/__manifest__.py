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
  "name"                 :  "Odoo Marketplace Seller Blogs",
  "summary"              :  """Sellers in marketplace can manage their own blogs and customers can view their blogs.""",
  "category"             :  "website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Marketplace-Seller-Blogs.html",
  "description"          :  """https://webkul.com/blog/odoo-marketplace-seller-blogs/""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_seller_blogs&version=13.0&lifetime=120&lout=1&custom_url=/",
  "depends"              :  [
                             'odoo_marketplace',
                             'website_blog',
                            ],
  "data"                 :  [
                             'security/access_control_security.xml',
                             'security/ir.model.access.csv',
                             'views/templates.xml',
                             'views/seller_view.xml',
                             'views/blog_tags_views.xml',
                             'views/seller_blog_res_config_view.xml',
                             'views/seller_blog_views.xml',
                             'views/seller_profile_seller_blog_template.xml',
                             'views/inherit_snippets.xml',
                             'views/inherit_mp_dashboard.xml',
                             'data/blog_blog_seller_blog_demo_data.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  30,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}