#  -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models, _
from odoo.http import request
from datetime import datetime, timedelta, date
import logging
_logger = logging.getLogger(__name__)


class Website(models.Model):
	_inherit = 'website'

	def wk_get_default_product(self):
		return self.env['ir.default'].sudo().get('res.config.settings', 'wk_coupon_product_id')

	@api.model
	def get_voucher_product_price(self, sale_order, voucher_obj, voucher_product_id):
		selected_prod_percent_price = 0
		order_total_price = 0
		for order_line_id in sale_order.order_line:
			if order_line_id.product_id.id != voucher_product_id and not order_line_id.is_delivery:
				order_total_price += order_line_id.product_uom_qty * order_line_id.price_unit
				if voucher_obj and voucher_obj.applied_on == 'specific':
					if order_line_id.product_id.product_tmpl_id.id in voucher_obj.product_ids.ids:
						selected_prod_percent_price += order_line_id.price_unit*order_line_id.product_uom_qty
		return {'selected_prod_percent_price':selected_prod_percent_price,'order_total_price':order_total_price}

	@api.model
	def set_voucher_sale_order_price(self, sale_order, voucher_obj, voucher_product_id, selected_prod_percent_price,coupon_id, order_total_price):
		for order_line_id in sale_order.order_line:
			if order_line_id.product_id.id == voucher_product_id:
				price_unit = 0
				if voucher_obj.customer_type == 'general':
					wk_voucher_value = voucher_obj.voucher_value
					if voucher_obj.voucher_val_type == 'amount':
						if voucher_obj.applied_on == 'specific':
							if selected_prod_percent_price > wk_voucher_value:
								price_unit = -wk_voucher_value
							else:
								price_unit = -selected_prod_percent_price
						else:
							if order_total_price >= wk_voucher_value:
								price_unit = -wk_voucher_value
							else:
								price_unit = -order_total_price
					else:
						if voucher_obj.applied_on == 'specific':
							price_unit = -((wk_voucher_value * selected_prod_percent_price) /100)
						else:
							price_unit = -((wk_voucher_value * order_total_price) /100)
				else:
					amount_left = 0
					history_objs = self.env['voucher.history'].search([('voucher_id','=',coupon_id)])
					if history_objs:
						for hist_obj in history_objs:
							if hist_obj.order_id and hist_obj.order_id.id == sale_order.id:
								continue
							amount_left += voucher_obj._get_amout_left_special_customer(hist_obj)
					if voucher_obj.voucher_val_type == 'amount':
						if voucher_obj.applied_on == 'specific':
							if selected_prod_percent_price >= amount_left:
								price_unit = -amount_left
							else:
								price_unit = -selected_prod_percent_price
						else:
							if order_total_price >= amount_left:
								price_unit = -amount_left
							else :
								price_unit = -order_total_price
					else:
						if voucher_obj.applied_on == 'specific':
							price_unit = -((amount_left * selected_prod_percent_price) /100)
						else:
							price_unit = -((amount_left * order_total_price) /100)
				order_line_id.price_unit = price_unit
		return True


	def get_current_order_voucher(self, order):
		voucher_product_id = self.env['ir.default'].sudo().get('res.config.settings', 'wk_coupon_product_id')
		coupon = order.order_line.filtered(lambda x: x.product_id.id == voucher_product_id)
		if coupon:
			return coupon[0].wk_voucher_id
		return False


	@api.model
	def sale_get_order(self, force_create=False, code=None, update_pricelist=False, force_pricelist=False, context=None):
		sale_order = super(Website, self).sale_get_order(force_create, code, update_pricelist, force_pricelist)
		order_total_price = 0
		voucher_obj = self.get_current_order_voucher(sale_order)
		if voucher_obj:
			if hasattr(sale_order,'order_line'):
				voucher_product_id = self.wk_get_default_product()
				if isinstance(voucher_product_id, (list)):
					voucher_product_id = voucher_product_id[0]
				res = self.get_voucher_product_price(sale_order,voucher_obj, voucher_product_id)
				selected_prod_percent_price = res['selected_prod_percent_price']
				order_total_price = res['order_total_price']
				self.set_voucher_sale_order_price(sale_order, voucher_obj,voucher_product_id, selected_prod_percent_price,voucher_obj.id,order_total_price)
		return sale_order

	def wk_get_customer_vouchers(self):
		partner_id = self.env['res.users'].browse(self._uid).partner_id.id
		current_date = datetime.now().date()
		voucher_ids = self.env['voucher.voucher'].search([('expiry_date','>=',current_date),('issue_date','<=',current_date),('customer_type','=','general'),('voucher_usage','!=','pos')])
		voucher_ids += self.env['voucher.voucher'].search([('expiry_date','>=',current_date),('issue_date','<=',current_date),('customer_id','=',partner_id),('customer_type','=','special_customer'),('voucher_usage','!=','pos')])
		return voucher_ids


	def get_remained_voucher_value(self, voucher_obj):
		msg = ''
		rdm_msg = ''
		value_remained = True
		used_vouchers = 0
		total_availability = -1
		if voucher_obj.customer_type == 'special_customer':
			if voucher_obj.is_partially_redemed and voucher_obj.redeemption_limit != -1:
				if used_vouchers and  len(used_vouchers) >= voucher_obj.redeemption_limit:
					value_remained = False
					msg	= _('Voucher has been Redeemed to its maximum limit.')
			history_objs  = self.env['voucher.history'].search([('voucher_id','=',voucher_obj.id)])
			amount_left = 0
			for hist_obj in history_objs:
				amount_left += voucher_obj._get_amout_left_special_customer(hist_obj)
			if amount_left <= 0.0:
				value_remained = False
				msg	= _('You have redeemed this voucher already.You cannot redeem this voucher any more!!!')
			else:
				voucher_value = amount_left
				value_remained = True
				msg	= _('Total value left in this voucher is %s .')%voucher_value
			if voucher_obj.is_partially_redemed:
				if voucher_obj.redeemption_limit == -1:
					rdm_msg = 'You can partially redeem this voucher unlimited times.'
				elif voucher_obj.redeemption_limit == 1:
					rdm_msg = 'You can  redeem this voucher only once.'
				else:
					rdm_msg = 'You can partially redeem this voucher %s times.'%voucher_obj.redeemption_limit
		else:
			if voucher_obj.total_available == 0:
				total_availability = 0
				msg = 'Total availability of this voucher is zero, now you can not redeem this voucher anymore.'
		return {"msg":msg, 'value_remained':value_remained,'rdm_msg':rdm_msg, 'total_availability':total_availability}

	@api.model
	def get_expiry_date(self, voucher_id):
		return  datetime.strptime(str(voucher_id.expiry_date), '%Y-%m-%d').strftime('%d %b %Y')
