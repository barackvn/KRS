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
from datetime import date
from datetime import datetime, timedelta

import logging
_logger = logging.getLogger(__name__)

class SaleOrderline(models.Model):
	_inherit = "sale.order.line"

	def _check_eligibility_for_rma(self):
		config_setting = self.env["res.config.settings"].get_values()
		for obj in self:
			if obj.marketplace_seller_id:
				config_setting = {
					'days_for_rma' : obj.marketplace_seller_id.get_seller_global_fields('days_for_rma'),
					'rma_day_apply_on' : obj.marketplace_seller_id.get_seller_global_fields('rma_day_apply_on'),
				}
			create_date = None
			if config_setting.get("days_for_rma", False):
				if config_setting.get("rma_day_apply_on", False) and config_setting["rma_day_apply_on"] == "so_date":
					create_date = obj.create_date.date()
				if config_setting.get("rma_day_apply_on", False) and config_setting["rma_day_apply_on"] == "do_date":
					move_line = self.env["stock.move"].search(
                        [("product_id", "=", obj.product_id.id), ("group_id.sale_id", "=", obj.order_id.name)])

					if move_line and move_line[0].picking_id.date_done:
						done_date = move_line[0].picking_id.date_done.date()
						create_date = done_date
				days = timedelta(config_setting["days_for_rma"] or 0)
				today_date = datetime.today().date()
				if create_date:
					valid_upto = create_date + days
					if today_date <= valid_upto:
						obj.is_eligible_for_rma = True
			else:
				obj.is_eligible_for_rma = False
			obj.is_eligible_for_rma = False if create_date == None else True
