# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models, _
from odoo.tools.translate import _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

from logging import getLogger
_logger = getLogger(__name__)

class SaleAdvancePaymentInv(models.TransientModel):
	_inherit = "sale.advance.payment.inv"

	# @api.multi
	def _create_invoice(self, order, so_line, amount):
		invoice = super(SaleAdvancePaymentInv,self)._create_invoice(order=order,so_line=so_line,amount=amount)
		invoice.write({
			'wk_invoice_notes':order.wk_notes,
			'desired_delivery_date':order.wk_desire_date,
		})
		return invoice