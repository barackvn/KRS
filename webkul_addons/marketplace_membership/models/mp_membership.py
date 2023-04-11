# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
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
#################################################################################

from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning
from datetime import datetime, timedelta
from lxml import etree


import logging
_logger = logging.getLogger(__name__)

MP_MEMBERSHIP_STATE = [
    ('draft', 'Draft'),
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('old', 'Expired'),
    ('canceled', 'Cancelled'),
]

class SellerMembership(models.Model):
    _name = 'seller.membership'
    _rec_name = 'partner_id'
    _order = 'id desc'

    partner_id = fields.Many2one('res.partner', string='Seller', ondelete='cascade', index=True, domain="[('seller', '=', True)]")
    mp_membership_plan_id = fields.Many2one('product.product', string="Membership Plan", required=True, domain="[('wk_mp_membership', '=', True)]")
    mp_membership_date_from = fields.Date(string='Valid From')
    mp_membership_date_to = fields.Date(string='Expire On')
    mp_membership_cancel_date = fields.Date(string='Cancel date')
    date = fields.Date(string='Request Date', help="Date on which member has requested the membership")
    mp_membership_fee = fields.Float(string='Membership Fee', digits='Product Price', required=True, help='Amount for the membership.')
    no_of_product = fields.Integer("# of Allow Products", required="1", store=True)
    is_active = fields.Boolean("Active")

    #fields for related order
    order_line_id = fields.Many2one("sale.order.line", "Related Order Line")
    order_id = fields.Many2one("sale.order", "Related Order", related="order_line_id.order_id")

    #field for related invoice
    account_invoice_line_id = fields.Many2one('account.move.line', string='Account Invoice line', readonly=True, ondelete='cascade')
    account_invoice_id = fields.Many2one('account.move', related='account_invoice_line_id.move_id', string='Invoice', readonly=True, store=True)

    company_id = fields.Many2one('res.company', related='account_invoice_line_id.move_id.company_id', string="Company", readonly=True, store=True)

    state = fields.Selection(MP_MEMBERSHIP_STATE, compute='_compute_membership_state', string="Status",default='pending', search="_make_searchable_state", help="It indicates the membership status.\n"
             "-Draft: A membership has no invoice.\n"
             "-Pending: A member who has purchased/applied for the marketplace membership and whose invoice is going to be created or not paid yet.\n"
             "-Paid: A member who has paid the marketplace membership amount.\n"
             "-Expired: A member whose marketplace membership date has expired.\n"
             "-Cancelled: A member who has cancelled his marketplace membership.\n")

    _sql_constraints = [
        ('mp_membership_date_to_date_greater', 'check(mp_membership_date_to >= mp_membership_date_from)', 'Error ! Marketplace membership plan Expire On date cannot be before Valid From Date.')
    ]


    def _make_searchable_date_from(self, operator, value):
        self.env.cr.execute("""SELECT id FROM seller_membership""")
        all_seller_membership_ids = [dic["id"] for dic in self.env.cr.dictfetchall()]
        ids = [
            obj.id
            for obj in self.sudo().browse(all_seller_membership_ids)
            if obj.mp_membership_date_to == value
        ]
        return [('id', 'in', ids)]


    def _make_searchable_date_from(self, operator, value):
        self.env.cr.execute("""SELECT id FROM seller_membership""")
        all_seller_membership_ids = [dic["id"] for dic in self.env.cr.dictfetchall()]
        ids = [
            obj.id
            for obj in self.sudo().browse(all_seller_membership_ids)
            if obj.mp_membership_date_from == value
        ]
        return [('id', 'in', ids)]


    def _make_searchable_state(self, operator, value):
        self.env.cr.execute("""SELECT id FROM seller_membership""")
        all_seller_membership_ids = [dic["id"] for dic in self.env.cr.dictfetchall()]
        ids = [
            obj.id
            for obj in self.sudo().browse(all_seller_membership_ids)
            if obj.state == value
        ]
        return [('id', 'in', ids)]

    @api.depends('account_invoice_line_id.move_id.state',
                 'account_invoice_line_id.payment_id',
                 'account_invoice_line_id.move_id.type')
    def _compute_membership_state(self):
        """Compute the state lines """
        Invoice = self.sudo().env['account.move.line']
        today = fields.Date.today()
        for rec in self.sudo():
            active_membership =  self.sudo().search([('partner_id', '=', rec.partner_id.id), ('is_active','=',True)])
            _logger.info("====================TEsting===================%r",active_membership.read())
            if rec.account_invoice_id:
                inv_state = rec.account_invoice_id.state
                if inv_state == 'draft':
                    rec.state = 'pending'
                    rec.is_active = False
                elif inv_state == 'cancel' or rec.mp_membership_cancel_date:
                    rec.state = 'canceled'
                    rec.is_active = False
                elif inv_state == 'posted' :
                    if rec.mp_membership_date_from < today and rec.mp_membership_date_to < today and rec.mp_membership_date_from <= rec.mp_membership_date_to:
                        rec.state = "old"
                        rec.is_active = False
                    elif rec.mp_membership_date_to >= today and rec.mp_membership_date_from <= today:
                        rec.state = 'paid'
                        if not active_membership:
                            rec.is_active = True
                        invoices = Invoice.browse(rec.account_invoice_id.id).payment_id.mapped('invoice_ids')
                        if invoices.filtered(lambda invoice: invoice.type == 'out_refund'):
                            rec.state = 'canceled'
                            rec.is_active = False
                else:
                    rec.state = 'draft'
                    rec.is_active = False
            else:
                rec.state = 'draft'
                rec.is_active = False


    def membership_action_cancel(self):
        for rec in self:
            if rec.is_active:
                rec.sudo().mp_membership_cancel_date = fields.Date.today()
                rec.sudo().is_active = False
                seller_user = self.env["res.users"].sudo().search([('partner_id', '=', rec.partner_id.id)])
                pending_seller_group_obj = self.env.ref('odoo_marketplace.marketplace_draft_seller_group')
                seller_group_obj = self.env.ref('odoo_marketplace.marketplace_seller_group')
                if seller_user.has_group("odoo_marketplace.marketplace_draft_seller_group"):
                    # Remove seller user from draft seller group(marketplace_draft_seller_group)
                    seller_group_obj.sudo().write({"users": [(3, seller_user.id, 0)]})
                    # Add seller user to seller group(marketplace_seller_group)
                    pending_seller_group_obj.sudo().write({"users": [(4, seller_user.id, 0)]})



    def disable_all_make_active_membership(self):
        """ This method will activate current membership and disable all other membership for current seller."""

        self.ensure_one()
        if self:
            membership_objs = self.sudo().search([("partner_id", "=", self.partner_id.id)])
            membership_objs.write({"is_active": False})
            _logger.info("========================TEsting 222=================%r",[membership_objs.read(),self.read()])
            self.is_active = True
