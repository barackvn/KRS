# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################

from odoo import api, fields, models, _

class VoucherHistory(models.Model):
	_name = "voucher.history"
	_order = 'create_date desc'
	_description = "Voucher History"

	
	name = fields.Char('Voucher Name', size=100, required=True)
	voucher_id = fields.Many2one(comodel_name='voucher.voucher', string='Voucher')
	order_id = fields.Many2one(comodel_name='sale.order',string='Sale order')
	create_date = fields.Datetime(string='Date', help="Date on which voucher used or created.")
	sale_order_line_id = fields.Many2one(comodel_name='sale.order.line', string='Sale order line id')
	voucher_value = fields.Float(string='Voucher Value', required=True)
	user_id = fields.Many2one('res.partner', string='User')
	transaction_type = fields.Selection([('debit', 'Debit'),('credit', 'Credit')], string="Transaction Type" ,help="transaction type , when a coupon is redeemed its transaction type will be debit , and for the first  ")
	channel_used = fields.Selection([('pos', 'POS'),('ecommerce', 'Ecommerce'),('both', 'Both')], required=True, string="Channel" ,help="Channel by which voucher has been used.")
	description = fields.Text(String="Description")
	state = fields.Selection([
        ('draft','Draft'),
        ('done','Done'),
        ('fail','Failed')],
        default="draft",
        string='State')