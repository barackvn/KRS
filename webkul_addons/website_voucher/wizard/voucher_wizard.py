# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class VoucherWizard(models.TransientModel):
	_name = 'voucher.wizard' 	
	_description = "Voucher Wizard"
	voucher_code = fields.Char('Voucher Code', required=True)

	def validate_voucher_code(self):
		self.voucher_code
		self.ensure_one()
		result = {}
		if self._context['active_id']:
			active_obj = self.env['sale.order'].browse(self._context['active_id'])
			prod_ids =  []
			for line in active_obj.order_line:
				prod_ids.append(line.product_id.id)
			order_total = active_obj.amount_total
			result = self.env['voucher.voucher'].validate_voucher(self.voucher_code, order_total, prod_ids,refrence="ecommerce", partner_id=active_obj.partner_id.id)
			if not active_obj.order_line:
				raise UserError('There are not any products in this sale order. Please select at least one product.!!!')
			if result.get('product_id'):
				for line in active_obj.order_line:
					if line.product_id.id == result['product_id']:
						result['status'] = False
						result['message'] = 'You can use only one voucher per order'
		if not result['status']:
			raise UserError('%s'%result['message'])
		else:
			final_result = self.env['sale.order']._add_voucher(order_total, result, self._context['active_id'])
		return True

	