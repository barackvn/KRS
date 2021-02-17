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
import random
import logging
import json
import datetime
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools.misc import formatLang, format_date, get_lang
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.tools import float_is_zero
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class subscription_subscription(models.Model):

    _name = "subscription.subscription"
    _inherit = 'mail.thread'
    _description = "Subscription"
    _order = 'id desc'

    
    def unlink(self):
        for current_rec in self:
            if current_rec.invoice_ids:
                for invoice_id in current_rec.invoice_ids:
                    if invoice_id.state not in ('draft', 'cancel'):
                        raise UserError(
                            _("You can't delete the record because its invoice is create."))
            super(subscription_subscription, current_rec).unlink()
        return True

    @api.depends('invoice_ids')
    def get_invoiced_count(self):
        for rec in self:
            rec.invoice_count = len(rec.invoice_ids)

    @api.onchange('customer_name')
    def oncahnage_customer_name(self):
        if self.customer_name:
            self.customer_billing_address = self.customer_name

    
    @api.depends('start_date','start_immediately', 'trial_period','duration','unit')
    def get_end_date(self):
        end_date = ""
        for current_rec in self:
            if current_rec.num_billing_cycle > 0:
                date = current_rec.start_date
                if current_rec.unit == 'day':
                    end_date = date  + relativedelta(days = current_rec.duration)
                if current_rec.unit == 'month':
                    end_date = date + relativedelta(months = current_rec.duration)
                if current_rec.unit == 'year':
                    end_date = date + relativedelta(years = current_rec.duration)
                if current_rec.unit == 'week':
                    end_date = date + \
                        timedelta(weeks=current_rec.duration)
            current_rec.end_date = end_date

    
    def is_paid_subscription(self):
        for obj in self:
            if any(invoice.invoice_payment_state != 'paid' for invoice in obj.invoice_ids):
                obj.is_paid = True
            else:
                obj.is_paid = False


    is_paid = fields.Boolean(string="Is Paid", compute="is_paid_subscription")
    name = fields.Char(string='Name', readonly=True)
    active = fields.Boolean(string="Active", default=True)
    customer_name = fields.Many2one('res.partner', string="Customer Name", required=True)
    source = fields.Selection([('so','Sale Order'),('manual','Manual')],'Related To', default="manual")
    so_origin = fields.Many2one('sale.order', string="Order Ref" )
    subscription_ref = fields.Char(string="Subscription Ref",copy=False)
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True),('activate_subscription','=',True)], required=True)
    quantity = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    sub_plan_id = fields.Many2one('subscription.plan',  string="Subscription Plan", required=True)
    duration = fields.Integer(string="Duration",  required=True)
    unit = fields.Selection([('week','Week(s)'),('day','Day(s)'),('month','Month(s)'),('year','Year(s)')], string="Unit", required=True)
    price = fields.Float(string="Price",  required=True)
    start_date = fields.Date(string="Start Date", required=True)
    next_payment_date = fields.Datetime(string="Date of Next Payment",copy=False)
    state = fields.Selection([('draft','Draft'),('in_progress','In-progress'),('cancel','Cancelled'),('close','Finished'),('expired','Expired'),('renewed','Renewed')], default='draft', string='State', track_visibility="always",copy=False)
    reason = fields.Char(string="Reason", track_visibility="onchange")
    invoice_ids = fields.Many2many("account.move", string='Invoices', readonly=True, copy=False)
    invoice_count =  fields.Integer(compute="get_invoiced_count", readonly=True, string='Invoices')
    tax_id = fields.Many2many('account.tax', string='Taxes')
    num_billing_cycle = fields.Integer(string="No of Billing Cycle")
    start_immediately = fields.Char(string="Start")
    trial_duration = fields.Integer(string='Trial Duration')
    trial_duration_unit = fields.Selection([('week','Week(s)'),('day','Day(s)'),('month','Month(s)'),('year','Year(s)')],string='Unit', help="The trial unit specifpriceied in a plan. Specify  day, month, year.")
    trial_period = fields.Boolean(string="Plan has trial period", help="A value indicating whether a subscription should begin with a trial period.")
    subscription_id = fields.Many2one('subscription.subscription', string="Subscription Id", copy=False)
    customer_billing_address = fields.Many2one('res.partner', string="Customer Invoice/Billing Address")
    old_customer_id = fields.Many2one("res.partner", string="Old Customer")
    end_date = fields.Date(compute="get_end_date", string="End Date")
    currency_id = fields.Many2one('res.currency', string='Currency',default=lambda self:self.env.user.company_id.currency_id)

    so_line = fields.Many2one('sale.order.line',string='sale order line')

    _sql_constraints = [
    ('check_for_uniq_subscription', 'Check(1=1)', "You can't create Multiple Subscription for sale order with the same product and customer."),
    ]

    
    def write(self, vals):
        if vals.get('customer_name'):
            for current_rec in self:
                vals['old_customer_id'] = current_rec.customer_name.id
        return super(subscription_subscription, self).write(vals)

    
    def get_confirm_subscription(self):
        for current_rec in self:
            if not current_rec.active:
                raise UserError(_("You can't confirm an Inactive Subscription."))
            current_rec.state = 'in_progress'
            if  current_rec.source =='manual':
                current_rec.action_invoice_create()
            elif (current_rec.source =='so' or current_rec.source =='website') and current_rec.so_origin.invoice_count!=0:
                current_rec.action_invoice_create()



    @api.model
    def create_automatic_invoice(self):
        subscrptions = self.search([('start_date','<=', fields.Datetime.now()),('state','=','in_progress'),('next_payment_date','<=',fields.Datetime.now())])
        for subscription in subscrptions:
            subscription.action_invoice_create()
            

    @api.onchange('trial_period','trial_duration_unit','trial_duration' )
    def onchange_trial_period(self):
        date = datetime.today().date()
        if self.trial_period:
            if self.trial_duration_unit == 'day':
                date = date  + relativedelta(days = self.trial_duration)
            if self.trial_duration_unit == 'month':
                date = date + relativedelta(months = self.trial_duration)
            if self.trial_duration_unit == 'year':
                date = date + relativedelta(years = self.trial_duration)
            if self.trial_duration_unit == 'week':
                date = date + timedelta(weeks=self.trial_duration)
            if self.trial_duration_unit == 'hour':
                date = date + timedelta(hours = self.trial_duration)
        self.start_date = date

    
    def action_view_invoice(self):
        invoices = self.mapped('invoice_ids')
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_type': 'out_invoice',
        }
        if len(self) == 1:
            context.update({
                'default_partner_id': self.customer_name.id,
                'default_partner_shipping_id': self.so_origin.partner_shipping_id.id if self.so_origin else False,
                'default_invoice_payment_term_id': self.so_origin.payment_term_id.id if self.so_origin else False,
                'default_invoice_origin': self.mapped('name'),
                'default_user_id': self.so_origin.user_id.id if self.so_origin else False,
            })
        action['context'] = context
        return action

    
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        journal_id = self.env['account.move'].default_get(['journal_id'])['journal_id']
        name = fiscal_position_id = pos_id = False
        acc = self.customer_name.property_account_receivable_id.id
        if not journal_id:
            raise UserError(_('Please define an accounting sale journal for this company.'))
        if self.source in ['api','manual']:
            fiscal_position_id = self.customer_name.property_account_position_id.id
        invoice_vals = {
            'ref': self.so_origin.name or '' if self.source == 'so' else name,
            'invoice_origin': self.name,
            'type': 'out_invoice',
            'invoice_line_ids':[],
            'partner_id': self.customer_name.id,
            'journal_id': journal_id,
            'currency_id': self.so_origin.pricelist_id.currency_id.id or self.currency_id.id,
            'invoice_payment_term_id': self.so_origin.payment_term_id.id or '',
            'fiscal_position_id': self.so_origin.fiscal_position_id.id or self.so_origin.partner_invoice_id.property_account_position_id.id if self.source == 'so' else fiscal_position_id,
            'company_id': self.so_origin.company_id.id if self.source == 'so' else self.env.company,
            'invoice_user_id': self.so_origin.user_id and self.so_origin.user_id.id if self.source == 'so' else self._uid,
            'is_subscription' : True,
        }
        return invoice_vals


    def cal_date_period(self,start_date,end_date,billing_cycle):
        date_diff = (end_date - start_date).days
        hour_diff = date_diff*24
        return [(start_date + relativedelta(hours=i)).strftime("%d/%m/%Y %H:%M:%S") for i in range(1,hour_diff,hour_diff//self.num_billing_cycle)][1:]

    
    def action_invoice_create(self, grouped=False, final=False):
        inv_obj = self.env['account.move']
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        invoices = {}
        for subscription in self:
            if not subscription.active:
                raise UserError(_("You can't generate invoice of an Inactive Subscription."))
            if subscription.state == 'draft':
                raise UserError("You can't generate invoice of a subscription which is in draft state, please confirm it first.")
            if subscription.trial_period:
                if subscription.start_date > datetime.today().date():
                    subscription.next_payment_date = datetime(*subscription.start_date.timetuple()[:6])
                    wizard_id = self.env['subscription.message.wizard'].create({'message':"You can't create invoice for this subscription because, its in a trial period."})
                    return {
                        'name': _("Message"),
                            'view_mode': 'form',
                            'view_id': False,
                            'view_type': 'form',
                            'res_model': 'subscription.message.wizard',
                            'res_id': wizard_id.id,
                            'type': 'ir.actions.act_window',
                            'nodestroy': True,
                            'target': 'new',
                    }
            if subscription.num_billing_cycle == subscription.invoice_count or subscription.num_billing_cycle < subscription.invoice_count and subscription.num_billing_cycle != -1:
                subscription.state = 'expired'
                return True
            group_key = subscription.id if grouped else (subscription.customer_name.id, subscription.product_id.currency_id.id)
            if float_is_zero(subscription.quantity, precision_digits=precision):
                    continue
            if group_key not in invoices:
                inv_data = subscription._prepare_invoice()
            elif group_key in invoices and subscription.name not in invoices[group_key].so_origin.split(', '):
                invoices[group_key].write({'origin': invoices[group_key].origin + ', ' + subscription.name})
            if subscription.quantity > 0:
                invoice_lines = subscription.invoice_line_create(inv_data,subscription.quantity)
                invoice = inv_obj.create(invoice_lines)
                invoices[group_key] = invoice
                
        if invoices:
            message = 'Invoice Created'
            invoice_generated =  self.env["ir.default"].get('res.config.settings', 'invoice_generated')
            sent_invoice = self.env["ir.default"].get('res.config.settings', 'invoice_email')
            for inv in invoices.values():
                pass
            if self.invoice_ids:
                self.invoice_ids =  [(4,inv.id)]
            else:
                self.invoice_ids = [inv.id]
            if invoice_generated =='paid':
                invoice.make_payment(invoice_generated)                
                message = "Paid Invoice Created"
            elif invoice_generated =='post':
                invoice.make_payment(invoice_generated)                
                message = "Post Invoice Created"
            if sent_invoice:
                template = self.env.ref('account.email_template_edi_invoice')
                subjects = self.env['mail.template']._render_template(template.subject, 'account.move', invoice.id)
                body = template._render_template(template.body_html, 'account.move', invoice.id)
                emails_from = self.env['mail.template']._render_template(template.email_from,'account.move', invoice.id)
                mail_compose_obj = self.env['mail.compose.message'].create({
                    'subject':subjects,
                    'body':body,
                    'parent_id':False,
                    'email_from':emails_from,
                    'model':'account.move',
                    'res_id':invoice.id,
                    'record_name':invoice.name,
                    'message_type':'comment',
                    'composition_mode':'comment',
                    'partner_ids':[invoice.partner_id.id],
                    'auto_delete':False,
                    'template_id':template.id,
                    'add_sign':True,
                    'subtype_id':1,
                    'author_id':self.env.user.partner_id.id,
                })
                mail_compose_obj.with_context(custom_layout="mail.mail_notification_paynow",model_description='invoice').send_mail()
                self.mapped('invoice_ids').write({'invoice_sent': True})
            
            start_date = datetime(year=self.start_date.year, month=self.start_date.month, day=self.start_date.day, minute=0, hour=0, second=0) if self.source =='manual' else self.start_date + relativedelta(days = 1)

            if not isinstance(start_date,datetime):
                start_date = datetime(*start_date.timetuple()[:6])

            if subscription.num_billing_cycle != subscription.invoice_count:
                if self.num_billing_cycle>0:

                    end_date = datetime(year=self.end_date.year, month=self.end_date.month, day=self.end_date.day, minute=0, hour=0, second=0) 
                    date_intervals = self.cal_date_period(start_date,end_date,self.num_billing_cycle)
                    self.next_payment_date = datetime.strptime(date_intervals[self.invoice_count-1],"%d/%m/%Y %H:%M:%S")
                else:
                    end_date = start_date if not self.next_payment_date else self.next_payment_date
                    if self.unit == 'day':
                        end_date = end_date  + relativedelta(days = self.duration)
                    if self.unit == 'month':
                        end_date = end_date + relativedelta(months = self.duration)
                    if self.unit == 'year':
                        end_date = end_date + relativedelta(years = self.duration)
                    if self.unit == 'week':
                        end_date = end_date + timedelta(weeks = self.duration)
                    self.next_payment_date = end_date
            else:
                self.next_payment_date = self.end_date
                
            wizard_id = self.env['subscription.message.wizard'].create({'message':message})
        else:
            wizard_id = self.env['subscription.message.wizard'].create({'message':'Subscription Expired.'})
        return {
            'name': _("Message"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'subscription.message.wizard',
                'res_id': wizard_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
        }

    


    
    def _prepare_invoice_line(self, qty):
        self.ensure_one()
        product = self.product_id.with_context(
            lang=self.customer_name.lang,
            partner=self.customer_name.id,
            quantity=self.quantity,
            date=self.start_date,
            pricelist=self.so_origin.pricelist_id if self.so_origin else False,
            uom=self.product_id.uom_po_id.id or False
        )
        name = product.name_get()[0][1]
        if product.description_sale:
            name += '\n' + product.description_sale
        res = {}
        account = self.product_id.property_account_income_id or self.product_id.categ_id.property_account_income_categ_id
        if not account:
            raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') % \
                            (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))
        fpos = self.customer_name.property_account_position_id
        if fpos:
            account = fpos.map_account(account)
        res = {
            'name': name,
            'account_id': account.id,
            'price_unit': self.price,
            'quantity': self.quantity,
            'product_id': self.product_id.id or False,
            'tax_ids': [(6, 0, self.tax_id.ids)],
        }
        return res

    
    def invoice_line_create(self, inv_data, qty):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for line in self:
            if not float_is_zero(qty, precision_digits=precision):
                vals = line._prepare_invoice_line(qty=qty)
                inv_data['invoice_line_ids'].append((0,0,vals))
                return inv_data

    
    def pay_cancel_invoice(self):
        for current_rec in self:
            for invoice_id in current_rec.invoice_ids:
                if invoice_id.state == 'draft':
                    res = invoice_id.button_cancel()
                elif invoice_id.state == 'posted' and invoice_id.invoice_payment_state != 'paid':
                    journal_id =  self.env["ir.default"].get('res.config.settings', 'journal_id')
                    # is_paid_invoice =  self.env["ir.default"].get('res.config.settings', 'is_paid_invoice')
                    # if not is_paid_invoice:
                    invoice_id.button_draft()
                    invoice_id.button_cancel()
        return True

    
    def get_cancel_sub(self):
        for current_rec in self:
            if current_rec.state == 'draft':
                current_rec.state = 'cancel'
        return True

    
    def make_payment(self):
        journal_id =  self.env["ir.default"].get('res.config.settings', 'journal_id')
        if not journal_id:
            raise UserError(_("Default Journal not found."))
        journal = self.env['account.journal'].browse(journal_id)
        for current_rec in self:
            if current_rec.invoice_ids:
                for invoice_id in current_rec.invoice_ids:
                    if invoice_id.amount_residual_signed > 0.0:
                        invoice_id.action_post()
                        if not invoice_id.journal_id.default_credit_account_id:
                            invoice_id.journal_id.default_credit_account_id =  self.env.ref('subscription_management.subscription_sale_journal').id 
                        self.env['account.payment'].sudo().create({'journal_id':invoice_id.journal_id.id,'amount':invoice_id.amount_total,'payment_date':invoice_id.invoice_date,'communication':invoice_id.name,'payment_type':'inbound','payment_method_id':self.env['account.payment.method'].search([('payment_type', '=', 'inbound')], limit=1).id,'partner_type':'customer','partner_id':invoice_id.partner_id.id,}).post()
                        invoice_id.invoice_payment_state = 'paid'
                        invoice_id.amount_residual= invoice_id.amount_total-invoice_id.amount_residual
                        invoice_id.amount_residual_signed = invoice_id.amount_total-invoice_id.amount_residual_signed
                        invoice_id._compute_payments_widget_reconciled_info()
                           
        return True

    
    def reset_to_draft(self):
        for current_rec in self:
            if current_rec.state == 'cancel':
                current_rec.state = 'draft'
        return True

    
    def reset_to_close(self):
        for current_rec in self:
            if current_rec.state not in ['close','cancel','renewed']:
                if current_rec.invoice_ids:
                    self.pay_cancel_invoice()
                current_rec.state = 'close'
                current_rec.num_billing_cycle = current_rec.invoice_count
            if self._context.get('close_refund'):
                return current_rec.action_view_invoice()
        return True

    @api.model
    def create(self, vals):
        vals['name'] =  self.env['ir.sequence'].next_by_code('subscription.subscription')

        if not vals.get('customer_billing_address'):
            vals['customer_billing_address'] = vals.get('customer_name')

        trial_period_setting = self.env['res.config.settings'].sudo().get_values()['trial_period_setting']
        if len(self.env['res.partner'].sudo().browse(vals['customer_name']).all_subscription)!=0 and trial_period_setting=='one_time':
            if vals.get('trial_period'):
                vals['trial_period']=False
                vals.pop('trial_duration_unit',None)
                vals.pop('trial_duration',None)
                vals['start_date'] = datetime.today().date()
        elif trial_period_setting=='product_based' and self.env['res.partner'].sudo().browse(vals['customer_name']).all_subscription.filtered(lambda subscription:subscription.product_id.id==vals['product_id']):
            if vals.get('trial_period'):
                vals['trial_period']=False
                vals.pop('trial_duration_unit',None)
                vals.pop('trial_duration',None)   
                vals['start_date'] = datetime.today().date()
        res = super(subscription_subscription, self).create(vals)
        return res


    @api.onchange('so_origin')
    def onchange_sale_order(self):
        result = {}
        product_id = []
        for order_line in self.so_origin.order_line:
            if order_line.product_id.activate_subscription:
                self.product_id = order_line.product_id.id
                self.tax_id = [(6, 0, order_line.tax_id.ids)]

    @api.onchange('product_id')
    def onchange_product_id(self):
        result = {}
        if self.product_id:
            self.sub_plan_id = self.product_id.subscription_plan_id.id
            self.price = self.product_id.lst_price
            self.tax_id = [(6,0, self.product_id.taxes_id.ids)]

    @api.onchange('sub_plan_id')
    def onchange_subscription_plan(self):
        if self.sub_plan_id:
            date = datetime.today()
            if self.sub_plan_id.trial_period:
                if self.sub_plan_id.trial_duration_unit == 'day':
                    date = date  + relativedelta(days = self.sub_plan_id.trial_duration)
                if self.sub_plan_id.trial_duration_unit == 'month':
                    date = date + relativedelta(months = self.sub_plan_id.trial_duration)
                if self.sub_plan_id.trial_duration_unit == 'year':
                    date = date + relativedelta(years = self.sub_plan_id.trial_duration)
                if self.sub_plan_id.trial_duration_unit == 'week':
                    date = date + timedelta(weeks = self.sub_plan_id.trial_duration)
                if self.sub_plan_id.trial_duration_unit == 'hour':
                    date = date + timedelta(hours = self.sub_plan_id.trial_duration)
            self.trial_period = self.sub_plan_id.trial_period
            self.trial_duration_unit = self.sub_plan_id.trial_duration_unit
            self.trial_duration = self.sub_plan_id.trial_duration
            self.num_billing_cycle = self.sub_plan_id.num_billing_cycle
            self.duration = self.sub_plan_id.duration
            self.unit = self.sub_plan_id.unit
            self.start_date = date.date()
            # self.next_payment_date = date
            if not self.sub_plan_id.override_product_price:
                self.price = self.sub_plan_id.plan_amount

    
    def renewe_subscription(self):
        for current_rec in self:
            if current_rec.state in ['expired','close']:
                current_rec.create_subscription()
                wizard_id = self.env['subscription.message.wizard'].create({'message':'Subscription Renewed.'})
                return {
                    'name': _("Message"),
                    'view_mode': 'form',
                    'view_id': False,
                    'view_type': 'form',
                    'res_model': 'subscription.message.wizard',
                    'res_id': wizard_id.id,
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'new',
                }
            return False

    
    def create_subscription(self):
        date = datetime.today().date()
        res = self.copy()
        res.start_date = date
        res.subscription_id = self.id
        self.state = "renewed"
        return res


   

