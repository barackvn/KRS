# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CreditLimitExceedWizard(models.TransientModel):
    _name = 'credit.limit.exceed.wizard'
    _description = 'Credit limit exceed wizard'

    order_id = fields.Many2one('sale.order')
    partner_id = fields.Many2one('res.partner',
                                 related='order_id.partner_id',
                                 readonly=1)
    partner_currency_id = fields.Many2one(
        'res.currency', related='order_id.partner_id.currency_id', readonly=1)
    credit_limit = fields.Float('Credit Limit',
                                related='order_id.partner_id.credit_limit',
                                currency_field='partner_currency_id',
                                readonly=1)
    order_amount = fields.Monetary('Order Amount',
                                   currency_field='partner_currency_id',
                                   readonly=1)

    pending_amount = fields.Monetary('Unpaid Amount',
                                     currency_field='partner_currency_id',
                                     readonly=1)
    overdue_invoice_amount = fields.Monetary(
        'Overdue Amount', currency_field='partner_currency_id', readonly=1)
    exceeded_credit = fields.Monetary('Exceeded Amount',
                                      currency_field='partner_currency_id',
                                      readonly=1)

    pending_invoice_ids = fields.Many2many('account.move',
                                           string='Pending invoices',
                                           readonly=1)
    unpaid_order_ids = fields.Many2many('sale.order',
                                        string='Sale orders (Unpaid)',
                                        readonly=1)

    message = fields.Char('Message')

    def action_exceed_limit(self):
        self.ensure_one()
        order = self.order_id
        if self.env.user.has_group('sales_team.group_sale_manager'):
            # Skip approval process for Sale Managers
            order.action_approve()
        else:
            if order.user_id:
                salesPerson = order.user_id
            else:
                salesPerson = self.env.user
            if not salesPerson.partner_id.email:
                raise UserError(
                    "Please add your email for related partner of your user %s ."
                    % (salesPerson.name))

            employee = salesPerson.employee_ids[0] if salesPerson.employee_ids else False

            if salesPerson.employee_ids:
                managerEmployeeId = salesPerson.employee_ids[0].parent_id
                if managerEmployeeId:
                    if managerEmployeeId.user_id:
                        managerPartner = managerEmployeeId.user_id.partner_id
                        order.message_subscribe([managerPartner.id])
                        if not managerPartner.email:
                            raise UserError(
                                "Please ask your admin to add email of employee %s on employee portal."
                                % (managerEmployeeId.name))
                    else:
                        raise UserError(
                            "Please ask your admin to add related user of employee %s on employee portal."
                            % (managerEmployeeId.name))
                else:
                    raise UserError(
                        "Please ask your admin to add manager of employee %s on employee portal."
                        % (employee.name))
            else:
                raise UserError(
                    "Please ask your admin to configure %s on employee portal."
                    % (salesPerson.name))

            # Set order 'To Approve' and notify manager
            order.state = 'need_approval'

            credit_limit = '%.2f' % self.credit_limit
            pending_amount = '%.2f' % self.pending_amount
            overdue_invoice_amount = '%.2f' % self.overdue_invoice_amount
            order_amount = '%.2f' % self.order_amount
            exceeded_credit = '%.2f' % self.exceeded_credit
            symbol = self.partner_currency_id.symbol
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

            subject = 'Approval for order %s requested by %s' % (order.name, salesPerson.name)
            message = """
            Hi %s,<br/><br/>
            The Sales Order %s needs your approval because <i><b>%s</b></i>
            <ul>
                <li>Customer: %s</li>
                <li>Credit Limit: %s %s</li>
                <li>Unpaid Amount: %s %s</li>
                <li>Overdue Amount: %s %s</li>
                <li>Order Amount: %s %s</li>
                <li>Exceeded Credit: <span style="color:red">%s %s</span></li>
            </ul>
            <p>
                <a href="%s/mail/view?model=%s&amp;res_id=%s"
                        style="background-color: #9E588B; margin-top: 10px; padding: 10px; text-decoration: none; color: #fff; border-radius: 5px; font-size: 16px;">
                    View %s
                </a>
            </p>
            Thanks & Regards,<br/>
            %s
            """ % (managerEmployeeId.name, order.name, self.message,
                   self.partner_id.display_name, credit_limit, symbol,
                   pending_amount, symbol, overdue_invoice_amount, symbol,
                   order_amount, symbol, exceeded_credit,
                   symbol, base_url, order._name, order.id,
                   order._description.lower(), salesPerson.name)

            order.message_post(body=message, subject=subject)

            values = {
                'email_from': salesPerson.partner_id.email,
                'email_to': managerPartner.email,
                'subject': subject,
                'body_html': message,
                'auto_delete': True,
            }
            mail = self.env['mail.mail'].create(values)
            mail.send()
