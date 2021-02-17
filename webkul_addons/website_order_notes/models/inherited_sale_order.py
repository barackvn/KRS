# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import models, fields
# from odoo import SUPERUSER_ID

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	def _get_visibility(self):
		# res = dict.fromkeys(ids, 0)
		show_desire_date = self.website_id.wk_show_desire_date
		show_notes_input = self.website_id.wk_show_notes_input
		if show_desire_date:
			if show_notes_input:
				temp = 1
			else:
				temp = 2
		else:
			if show_notes_input:
				temp = 3
			else:
				temp = 4
		for record in self:
			_logger.info("---------temp-------%r",temp)
			record.visibility_value = temp



	visibility_value = fields.Integer(compute = _get_visibility, string="Visibility Value",  method=True)
	wk_notes  = fields.Text(string='Notes')
	wk_desire_date =  fields.Char(string="Desired Delivery date")
