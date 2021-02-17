# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################

from odoo import api, fields, models, _

class AddProduct(models.TransientModel):

    _name = "add.product"
    _description = "Add product for sale order line."

    product_id =  fields.Many2one('product.product',string='Product', domain=[('sale_ok', '=', True),('activate_subscription','=',True)], change_default=True, ondelete='restrict', required=True)
    trial_duration = fields.Integer(string='Trial Duration')
    trial_duration_unit = fields.Selection([('hour','Hour(s)'),('week','Week(s)'),('day','Day(s)'),('month','Month(s)'),('year','Year(s)')],string='Unit', help="The trial unit specified in a plan. Specify hour, day, month, year.")
    trial_period = fields.Boolean(string="Is plan has trail period", help="A value indicating whether a subscription should begin with a trial period.")
    num_billing_cycle = fields.Integer(string="No of Billing Cycle")
    month_billing_day = fields.Integer(string="Billing day of month", help="The value that specifies the day of the month that the gateway will charge the subscription on every billing cycle")

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id.activate_subscription:
            self.trial_period = self.product_id.subscription_plan_id.trial_period
            self.trial_duration_unit = self.product_id.subscription_plan_id.trial_duration_unit
            self.trial_duration = self.product_id.subscription_plan_id.trial_duration
            self.num_billing_cycle = self.product_id.subscription_plan_id.num_billing_cycle
            self.month_billing_day = self.product_id.subscription_plan_id.month_billing_day

            

    
    def create_sale_order_line(self):
        sale_order = self.env['sale.order'].browse(self._context.get('active_ids', []))
        product = self.product_id.with_context(
                    lang=sale_order.partner_id.lang,
                    partner=sale_order.partner_id.id,
                    quantity=1.0,
                    date=sale_order.date_order,
                    pricelist=sale_order.pricelist_id.id,
                    uom=self.product_id.uom_id.id
                )

        name = product.name_get()[0][1]
        if product.description_sale:
            name += '\n' + product.description_sale

        line_id = self.env['sale.order.line'].create({'product_id':self.product_id.id,'order_id':sale_order.id,'product_uom':self.product_id.uom_id.id,'name':name, 'price_unit':self.product_id.lst_price,'tax_id':[(6, 0, self.product_id.taxes_id.ids)]})
        if sale_order.pricelist_id and sale_order.partner_id:
            line_id.price_unit = self.env['account.tax']._fix_tax_included_price_company(self.product_id.lst_price, product.taxes_id, line_id.tax_id, line_id.company_id)
        return line_id
