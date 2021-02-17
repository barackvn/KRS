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

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_invoice_paid(self):
        res = super(AccountMove, self).action_invoice_paid()
        for rec in self:
            if rec.state == "posted":
                mp_membership_obj = self.env["seller.membership"].sudo().search([('account_invoice_id', '=', rec.id)])
                for mp_member in mp_membership_obj:
                    mp_member.disable_all_make_active_membership()
                    mp_membership_plan_dates = mp_member.mp_membership_plan_id.product_tmpl_id.get_mp_membership_plan_date_range()
                    if mp_membership_plan_dates:
                        mp_member.date_from = mp_membership_plan_dates.get("date_from", False)
                        mp_member.date_to = mp_membership_plan_dates.get("date_to", False)
        return res

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    
    def create(self, vals):
        
        invoice_line_obj = super(AccountMoveLine, self).create(vals)
        for obj in invoice_line_obj:
            mp_membership_obj = self.env['seller.membership'].sudo()
            
            _logger.info(obj.id )
            if obj.move_id.type == 'out_invoice' and obj.product_id.wk_mp_membership and not mp_membership_obj.search([('account_invoice_line_id', '=', obj.id)]):
                # Product in line is a marketplace membership product
                mp_membership_plan_dates = obj.product_id.product_tmpl_id.get_mp_membership_plan_date_range()
                date_from = mp_membership_plan_dates.get("date_from", False)
                date_to = mp_membership_plan_dates.get("date_to", False)
                if obj.move_id.invoice_date and obj.move_id.invoice_date > date_from and obj.move_id.invoice_date < date_to:
                    mp_membership_plan_dates = obj.product_id.product_tmpl_id.get_mp_membership_plan_date_range(date=obj.move_id.invoice_date)
                    date_from = mp_membership_plan_dates.get("date_from", False)
                    date_to = mp_membership_plan_dates.get("date_to", False)
                mp_membership_obj.sudo().create({
                    'partner_id': obj.move_id.partner_id.id,
                    'mp_membership_plan_id': obj.product_id.id,
                    'mp_membership_fee': obj.price_unit,
                    'date': fields.Date.today(),
                    'mp_membership_date_from': date_from,
                    'mp_membership_date_to': date_to,
                    'account_invoice_line_id': obj.id,
                    'no_of_product': obj.product_id.no_of_product,
                    'order_line_id': obj.sale_line_ids.ids[0] if obj.sale_line_ids else False
                })
                #Untick seller from Free member
                obj.move_id.partner_id.free_membership = False
                obj.move_id.message_partner_ids = [(4, obj.move_id.partner_id.id)]
        return invoice_line_obj
