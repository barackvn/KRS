# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import models, fields
# from odoo import SUPERUSER_ID

class stock_picking(models.Model):
	_inherit = "stock.picking"

	wk_picking_notes = fields.Text(string='Order Notes')