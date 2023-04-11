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

from odoo import models,fields,api

class Respartner(models.Model):
	_inherit = "res.partner"

	days_for_rma = fields.Integer(string="Return Policy",
		help="Number of days upto which customer can request for RMA after delivery done.")
	rma_day_apply_on = fields.Selection(
		[("so_date", "Order Date"),
		("do_date", "Delivery Date")],
		string="Apply On",
		default="do_date")


	@api.onchange("set_seller_wise_settings")
	def on_change_seller_wise_rma_settings(self):
		if self.set_seller_wise_settings:
			vals = {
				"days_for_rma": self.env['ir.default'].get(
					'res.config.settings', 'mp_days_for_rma'
				)
			}
			vals["rma_day_apply_on"] = self.env['ir.default'].get(
				'res.config.settings', 'mp_rma_day_apply_on')
			self.write(vals)
