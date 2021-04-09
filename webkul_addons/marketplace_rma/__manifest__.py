# -*- coding: utf-8 -*-
##########################################################################
# 2010-2017 Webkul.
#
# NOTICE OF LICENSE
#
# All right is reserved,
# Please go through this link for complete license : https://store.webkul.com/license.html
#
# DISCLAIMER
#
# Do not edit or add to this file if you wish to upgrade this module to newer
# versions in the future. If you wish to customize this module for your
# needs please refer to https://store.webkul.com/customisation-guidelines/ for more information.
#
# @Author        : Webkul Software Pvt. Ltd. (<support@webkul.com>)
# @Copyright (c) : 2010-2017 Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# @License       : https://store.webkul.com/license.html
#
##########################################################################

{
	"name"                 :  "Marketplace Retrun Merchandise Authorization (RMA)",
	"summary"              :  """Marketplace Return merchandise authorization module helps admin and sellers to manage product returns.""",
	"category"             :  "Marketplace",
	"version"              :  "1.0.0",
	"sequence"             :  1,
	"author"               :  "Webkul Software Pvt. Ltd.",
	"website"              :  "https://store.webkul.com/Odoo-Marketplace-RMA.html",
	"description"          :  """Marketplace RMA
Return merchandise authorization""",
	"live_test_url"        :  "http://odoodemo.webkul.com/?module=marketplace_rma&lifetime=120&lout=1&custom_url=/",
	"depends"              :  ['odoo_marketplace','rma'],
	"data"                 :  [
							'security/marketplace_rma_security.xml',
							'security/ir.model.access.csv',
							'wizard/product_return_view.xml',
							'wizard/new_delivery_order.xml',
							'views/rma_view.xml',
							'views/templates.xml',
							'views/marketplace_config_view.xml',
							'views/res_partner_view.xml',
							'data/mp_config_settings_data.xml',
							],
	"images"               :  ['static/description/Banner.png'],
	"application"          :  True,
  	"installable"          :  True,
  	"auto_install"         :  False,
	"price"                :  69,
	"currency"             :  "EUR",
	"application"          :  True,
	"pre_init_hook"        :  "pre_init_check",
}
