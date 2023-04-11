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
import datetime
from datetime import datetime, timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
from lxml import etree


import logging
_logger = logging.getLogger(__name__)

ColorList = [('1', "Green"), ('2', "Sky Blue"), ('3', "Blue"), ('4', "Cornsilk Yellow"), ('5', "Red"), ('6', "Default")]
BgColorList = {'1': "#dff0d8", '2': "#d9edf7", '3': "#337ab7", '4': "#fcf8e3", '5': "#f2dede", '6': "#f8f8f8"}
TextColorList = {'1' : "#3c763d", '2' : "#31708f", '3': "#fff", '4' : "#8a6d3b", '5' : "#a94442", '6':"#777777"}
BorderColorList = {'1' : "#d6e9c6", '2' : "#bce8f1", '3': "#337ab7", '4' : "#faebcc", '5' : "#ebccd1", '6':"#e7e7e7"}


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    wk_mp_membership = fields.Boolean(
        "MP Membership Plan", help='Check if the product is eligible for membership.')
    no_of_product = fields.Integer("# of Products Allow")
    plan_duration = fields.Integer("Plan Duration")
    duration_type = fields.Selection([('day', 'Days'), ('week', 'Weeks'), (
        'month', 'Months'), ('year', 'Years')], default="month")
    mp_membership_color = fields.Selection(ColorList, "Display Color")
    wk_tag_line = fields.Char("Tag Line")
    membership_t_and_c = fields.Text("Terms & Conditions", translate=True)

    _sql_constraints = [
        ('mp_membership_plan_duration', 'check(plan_duration >= 0)',
         'Error ! Plan duration can not be negative.')
    ]

    @api.onchange("no_of_product", "plan_duration", "duration_type")
    def onchange_membership_field(self):
        if self.wk_mp_membership:
            msg = "Under this membership plan you will get following features: \n"
            msg += "1. You can upload/create %s products.\n" % self.no_of_product
            msg += f"2. Duration for this will be {self.plan_duration} "
            msg += f"{self.duration_type}."
            self.description = self.description_sale = msg

    def get_mp_membership_plan_date_range(self, wk_date=None):
        """ Here: wk_date is a python date object not string."""

        self.ensure_one()
        if wk_date and isinstance(x, str):
            wk_date = datetime.datetime.strptime(wk_date, "%Y-%m-%d")
        if not wk_date:
            wk_date = date.today()
        result = {"date_from": str(wk_date)}
        duration_type = self.duration_type
        if duration_type == "month":
            months = self.plan_duration
            date_after_given_months = wk_date + relativedelta(months=+months)
            result["date_to"] = str(date_after_given_months)
        elif duration_type == "week":
            weeks = timedelta(weeks=self.plan_duration)
            date_after_given_weeks = wk_date + weeks
            result["date_to"] = str(date_after_given_weeks)
        elif duration_type == "year":
            years = self.plan_duration
            date_after_given_years = wk_date + relativedelta(years=+years)
            result["date_to"] = str(date_after_given_years)
        else:
            days = timedelta(days=self.plan_duration)
            date_after_given_days = wk_date + days
            result["date_to"] = str(date_after_given_days)
        return result

    def validate_product_limit(self, seller_id):
        seller_group = self.env['ir.model.data'].get_object_reference(
        'odoo_marketplace', 'marketplace_seller_group')[1]
        officer_group = self.env['ir.model.data'].get_object_reference(
        'odoo_marketplace', 'marketplace_officer_group')[1]
        groups_ids = self.env.user.sudo().groups_id.ids
        if officer_group in groups_ids and seller_id == self.env.user.partner_id.id:
            return True
        if seller_obj := self.env["res.partner"].browse(seller_id):
            seller_all_products = self.search([("marketplace_seller_id", "=", seller_obj.id)])
            if seller_obj.no_of_product <= len(seller_all_products):
                return False
        return True

    @api.model
    def create(self, vals):
        if vals.get("marketplace_seller_id", False) and not self.validate_product_limit(vals.get("marketplace_seller_id")):
            raise Warning(
                _("You can not create new product because you have not enough product limit. You need to purchase marketplace membership plan according to your need."))
        
        if vals.get('wk_mp_membership',False):
            vals['status'] = 'approved'
        return super(ProductTemplate, self).create(vals)

    
    def write(self, vals):
        if vals.get("marketplace_seller_id", False) and not self.validate_product_limit(vals.get("marketplace_seller_id")):
            raise Warning(
                _("You can not create new product because you have not enough product limit. You need to purchase marketplace membership plan according to your need."))
        return super(ProductTemplate, self).write(vals)

    
    def copy(self, default=None):
        self.ensure_one()
        if self.marketplace_seller_id and not self.validate_product_limit(self.marketplace_seller_id.id):
            raise Warning(
                _("You can not create new product because you have not enough product limit. You need to purchase marketplace membership plan according to your need."))
        return super(ProductTemplate, self).copy(default=default)

    def get_mp_color(self, element):
        if not self or not element:
            return False
        if element == "border":
            return BorderColorList.get(self.mp_membership_color) or "#e7e7e7"
        elif element == "text":
            return TextColorList.get(self.mp_membership_color) or "#777777"
        else:
            return BgColorList.get(self.mp_membership_color) or "#f8f8f8"
