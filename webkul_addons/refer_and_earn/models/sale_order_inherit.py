# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################
import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
	_inherit = 'sale.order'


	redeemable_points= fields.Float(string='Used Referred Earn points',compute='_amount_all', store=True)
	use_re_epoints = fields.Boolean(string="Use Redeemable Points")
	redeemable_amount= fields.Float(string='Used Referred Earn points',compute='_compute_redeemable_amt')


	# @api.one
	def _compute_redeemable_amt(self):
		for order in self:
			order.redeemable_amount = float("-"+str(order.redeemable_points))


	@api.depends('order_line.price_total','use_re_epoints')
	def _amount_all(self):
		"""
		Compute the total amounts of the SO.
		"""
		result = super(SaleOrder, self)._amount_all()
		for order in self:
			redeemable_points = 0
			if order.use_re_epoints:
				if order.amount_total > order.partner_id.referral_earning or order.amount_total == order.partner_id.referral_earning:

					redeemable_points = order.partner_id.referral_earning
				else:
					redeemable_points = order.amount_total
			order.redeemable_points = redeemable_points
			order.update({
					'redeemable_points':redeemable_points,
					'amount_total': order.amount_untaxed + order.amount_tax - redeemable_points,
				})


	# @api.multi
	def action_confirm(self):
		result = super(SaleOrder, self).action_confirm()
		for order in self:
			if order.state == 'sale':
				txn = self.env['transaction.history'].sudo().search([('state','=','draft'),('first_sale_order_id','=',order.id)])
				for t in txn:
					if t.state == 'draft':
						t.state = 'approve'


	# @api.multi
	def action_cancel(self):
		result = super(SaleOrder, self).action_cancel()
		for order in self:
			txn = self.env['transaction.history'].sudo().search([('state','=','draft'),('first_sale_order_id','=',order.id)])
			for t in txn:
				if t.state == 'draft':
					t.state = 'cancel'
