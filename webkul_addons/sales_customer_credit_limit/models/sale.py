# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.http import request


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('need_approval', 'To Approve'), ('sale', 'Sale Order')])

    def action_confirm(self):
        ctx = dict(self.env.context or {})
        txId = request.session.get('sale_transaction_id')
        if 'force_confirm' not in ctx and not txId:
            res = self.check_credit_limit()
            if res:
                return res
        elif txId:
            self.message_post(
                body="<b>Order is placed from website</b> so that credit limit module flow is ignored during order confirmation.")
        else:
            self.send_approval_mail()
        return super(SaleOrder, self).action_confirm()

    def send_approval_mail(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        currentUser = self.env.user
        for order in self:
            salesPerson = order.user_id

            if not salesPerson or salesPerson == currentUser:
                continue

            if not salesPerson.partner_id.email:
                raise UserError("Please add your email for related partner of your user %s ." % (salesPerson.name))

            subject = 'Order %s has been approved by %s' % (order.name, currentUser.name)
            message = """
            Hi %s,<br/><br/>
            The Sales Order %s has been approved. You can proceed for further actions.
            <p>
                <a href="%s/mail/view?model=%s&amp;res_id=%s" style="background-color: #9E588B; margin-top: 10px; padding: 10px; text-decoration: none; color: #fff; border-radius: 5px; font-size: 16px;">
                    View %s
                </a>
            </p><br/>
            Thanks & Regards,<br/>
            %s
            """ % (salesPerson.name, order.name, base_url, order._name,
                   order.id, order._description.lower(), currentUser.name)

            order.message_post(body=message, subject=subject)

            values = {
                'email_from': currentUser.partner_id.email,
                'email_to': salesPerson.partner_id.email,
                'subject': subject,
                'body_html': message,
                'auto_delete': True,
            }
            mail = self.env['mail.mail'].create(values)
            mail.send()

    def action_approve(self):
        if not self._check_access_to_approve():
            raise UserError("You do not have the rights to approve this Sale Order.")
        self.with_context({'force_confirm': True}).action_confirm()

    def _check_access_to_approve(self):
        if self.env.user.has_group('sales_team.group_sale_manager'):
            return True
        manager = self.env.user.employee_ids and self.env.user.employee_ids[0]
        if not manager:
            return False
        for order in self:
            salesPerson = order.user_id.employee_ids and order.user_id.employee_ids[0]
            if not salesPerson or not salesPerson.parent_id or manager != salesPerson.parent_id:
                return False
        return True

    def action_draft(self):
        orders = self.filtered(lambda s: s.state in ['need_approval'])
        orders.write({
            'state': 'draft',
        })
        return super(SaleOrder, self).action_draft()

    def check_credit_limit(self):
        openInvoiceIds, overdueInvoices = [], []
        orderAmount = openInvoiceAmount = overdueInvoiceAmount = excessAmount = 0
        message = ""
        orderPartner = self.partner_id
        if orderPartner.is_company or not orderPartner.parent_id:
            partner = orderPartner
        else:
            partner = orderPartner.commercial_partner_id

        partnerCurrencyId = partner.currency_id
        creditLimitAmount = partner.credit_limit
        if not creditLimitAmount:
            return False
        orderAmount = self.currency_id._convert(self.amount_total, partnerCurrencyId,
                                                self.company_id, self.date_order)

        openInvoices = self.env['account.move'].search([
            ('type', '=', 'out_invoice'),
            ('company_id', '=', self.company_id.id),
            ('state', 'not in', ['cancel']),
            ('partner_id', 'child_of', partner.id),
            ('invoice_payment_state', 'not in', ['paid']),
        ])
        openInvoiceIds = openInvoices.filtered(
            lambda i: i.invoice_payment_state != 'paid').ids
        openInvoiceAmount = sum(openInvoices.mapped('amount_residual_signed'))

        # Total amout which is invoiced but not paid (Draft invoices + unpaid amout in open invoices.)
        remainingInvoicesAmount = openInvoiceAmount

        confirmedOrders = self.env['sale.order'].search([
            '|', '&', ('state', 'in', ['sale', 'done']),
            ('invoice_status', 'in', ['to invoice']),
            ('state', 'in', ['need_approval']),
            ('company_id', '=', self.company_id.id),
            ('partner_id', 'child_of', partner.id),
        ])
        confirmedOrdersAmount = sum(
            confirmedOrders.mapped(lambda order: order.currency_id._convert(
                order.amount_total, partnerCurrencyId, self.company_id, order.
                date_order))) if confirmedOrders else 0.0

        confirmedOrdersInvoices = confirmedOrders.mapped(
            'invoice_ids').filtered(
                lambda invoice: invoice.type == 'out_invoice')
        confirmedOrdersInvoicesAmount = sum(
            confirmedOrdersInvoices.mapped('amount_total_signed'))

        # Total order amount for which invoice is not yet generated.
        remainingOrderAmount = confirmedOrdersAmount - confirmedOrdersInvoicesAmount

        totalPendingAmount = remainingOrderAmount + remainingInvoicesAmount

        if creditLimitAmount > 0:
            overdueInvoices = openInvoices.filtered(
                lambda inv: inv.invoice_date_due < fields.Date.today()
                if inv.invoice_date_due else True)
            excessAmount = orderAmount + totalPendingAmount - creditLimitAmount
            if excessAmount > 0:
                if (remainingInvoicesAmount):
                    message = "Total amount is exceeding from credit limit."
                else:
                    message = "This order amount is exceeding from credit limit."
            elif (overdueInvoices):
                overdueInvoiceAmount = sum(
                    overdueInvoices.mapped('amount_residual_signed'))
                message = "Invoices are overdue from it's scheduled date."
        elif openInvoices:
            overdueInvoices = openInvoices
            message = "Invoices are already open from the same customer for previous orders."
        elif remainingOrderAmount:
            message = "Customer is already having confirmed orders for which full invoice is not yet generated."

        if overdueInvoices or excessAmount > 0 or (creditLimitAmount <= 0 and remainingOrderAmount):
            wizardData = {
                'order_id': self.id,
                'pending_invoice_ids': [(6, 0, openInvoiceIds)],
                'overdue_invoice_amount': overdueInvoiceAmount,
                'unpaid_order_ids': [(6, 0, confirmedOrders.ids)],
                'pending_amount': totalPendingAmount,
                'exceeded_credit': excessAmount if excessAmount > 0 else 0,
                'order_amount': orderAmount,
                'message': message,
            }
            wizard = self.env['credit.limit.exceed.wizard'].create(wizardData)
            return {
                'type': 'ir.actions.act_window',
                'name': 'Customer Credit Limit info',
                'res_model': 'credit.limit.exceed.wizard',
                'res_id': wizard.id,
                'view_mode': 'form',
                'view_id': self.env.ref('sales_customer_credit_limit.credit_limit_exceed_wizard').id,
                'target': 'new',
            }
        return False
