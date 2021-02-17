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


import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models, _


class subscription_plan(models.Model):

    _name = "subscription.plan"
    _description = "Subscription Plan"

    name = fields.Char(string='Name', required=True)
    duration = fields.Integer(string='Duration', required=True)
    unit = fields.Selection([('week','Week(s)'),('day','Day(s)'),('month','Month(s)'),('year','Year(s)')],string='Unit', required=True, default='day')
    plan_amount = fields.Float(string="Price", required=True)
    plan_description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)
    override_product_price = fields.Boolean(string="Override product Price", help="Override the price of Product while creating product.", default="True")
    never_expires = fields.Boolean(string="Never Expire", help="This Plan billing cycle never expire instead of specifying a number of billing cycles.")
    num_billing_cycle = fields.Integer(string="Number Of Billing Cycles", help="Expire the plan after the given no. of Billing create")
    month_billing_day = fields.Integer(string="Billing day of month", help="The value that specifies the day of the month that the gateway will charge the subscription on every billing cycle")
    start_immediately = fields.Boolean(string="Start Immediately", help="This option helps to starts the subscription immediately.", default=True)
    trial_duration = fields.Integer(string='Trial Duration')
    trial_duration_unit = fields.Selection([('week','Week(s)'),('day','Day(s)'),('month','Month(s)'),('year','Year(s)')],string='Unit', help="The trial unit specified in a plan. Specify day, month, year.")
    trial_period = fields.Boolean(string="Plan has trial period", help="A value indicating whether a subscription should begin with a trial period.")
    subscription_ids = fields.One2many('subscription.subscription', 'sub_plan_id', string="Subscriptions")
    subscrption_count = fields.Integer(string='#', compute="get_subscription_count")
    product_ids = fields.One2many('product.product', 'subscription_plan_id', string="Products")
    product_count = fields.Integer(string='#', compute="get_product_count")
    color = fields.Integer(string='Color Index')

    
    def get_subscription_count(self):
        for obj in self:
            obj.subscrption_count = len(obj.subscription_ids.ids)

    
    def get_product_count(self):
        for obj in self:
            obj.product_count = len(obj.product_ids.ids)


    
    @api.depends('name', 'duration', 'unit')
    def name_get(self):
        result = []
        for subscription in self:
            name = subscription.name + ' (' + str(subscription.duration) + ' ' + subscription.unit + ' )'
            result.append((subscription.id, name))
        return result

    @api.onchange('trial_period')
    def onchange_trial_period(self):
        if self.trial_period:
            self.start_immediately = False

    @api.onchange('start_immediately')
    def onchange_start_immediately(self):
        if self.start_immediately:
            self.trial_period = False
            self.trial_duration = 0
            self.trial_duration_unit = ""

    @api.onchange('never_expires')
    def onchange_never_expires(self):
        num_billing_cycle = 0
        if self.never_expires:
            num_billing_cycle = -1
        self.num_billing_cycle = num_billing_cycle

    
    def action_view_subscription(self):
        subscription_ids = self.mapped('subscription_ids')
        action = self.env.ref('subscription_management.action_subscription').read()[0]
        action['context'] = {}
        if len(subscription_ids) > 1:
            action['domain'] = "[('id','in',%s)]" % subscription_ids.ids
        elif len(subscription_ids) == 1:
            action['views'] = [(self.env.ref('subscription_management.subscription_subscription_form_view').id, 'form')]
            action['res_id'] = subscription_ids.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action


    
    def action_view_products(self):
        product_ids = self.mapped('product_ids')
        action = self.env.ref('product.product_normal_action').read()[0]
        context = action.get('context')
        _logger.info('============%r',context)
        action['domain'] = "[('id','in',%s)]" % product_ids.ids
        if len(product_ids) > 1:
            action['domain'] = "[('id','in',%s)]" % product_ids.ids
        elif len(product_ids) == 1:
            action['views'] = [(self.env.ref('product.product_template_form_view').id, 'form')]
            action['res_id'] = product_ids.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action