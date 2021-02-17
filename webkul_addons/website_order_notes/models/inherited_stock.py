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

class StockMove(models.Model):
	_inherit = "stock.move"

	def _get_new_picking_values(self):
		res = super(StockMove, self)._get_new_picking_values()
		_logger.info(">>>>>>>>>>>>>>sale order>>>>>>%s>>>>>>>",self)
		move=''
		for rec in self:
			if not move:
				move=rec
		if move:
			order_id = self.env['sale.order'].sudo().search([('name','=',move.origin)], limit=1)
			if order_id:
				res['wk_picking_notes'] = order_id.wk_notes
		return res
