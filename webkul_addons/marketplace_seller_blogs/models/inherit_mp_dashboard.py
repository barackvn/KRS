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

from odoo import models, fields, api

class marketplace_dashboard(models.Model):
    _inherit = "marketplace.dashboard"

    def _get_approved_count(self):
        res = super(marketplace_dashboard, self)._get_approved_count()
        for rec in self:
            if rec.state == 'blogs':
                if rec.is_user_seller():
                    user_id = self.env['res.users'].search([('id', '=', rec._uid)])
                    seller_id = user_id.partner_id.id
                    obj = self.env['blog.post'].search([('marketplace_seller_id', '=', seller_id), ('website_published', '=', True)])
                else:
                    obj = self.env['blog.post'].search([('marketplace_seller_id', '!=', False), ('website_published', '=', True)])
                rec.count_product_approved = len(obj)

    def _get_pending_count(self):
        res = super(marketplace_dashboard, self)._get_pending_count()
        for rec in self:
            if rec.state == 'blogs':
                if rec.is_user_seller():
                    user_id = self.env['res.users'].search([('id', '=', rec._uid)])
                    seller_id = user_id.partner_id.id
                    obj = self.env['blog.post'].search([('marketplace_seller_id', '=', seller_id), ('website_published', '=', False)])
                else:
                    obj = self.env['blog.post'].search([('marketplace_seller_id', '!=', False), ('website_published', '=', False)])
                rec.count_product_pending = len(obj)

    state = fields.Selection(selection_add=[('blogs', 'Blogs')])
