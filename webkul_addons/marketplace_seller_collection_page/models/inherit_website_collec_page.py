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
from odoo.exceptions import UserError

def compute_login_userid(self):
    seller_group = self.env['ir.model.data'].get_object_reference(
    'odoo_marketplace', 'marketplace_seller_group')[1]
    officer_group = self.env['ir.model.data'].get_object_reference(
    'odoo_marketplace', 'marketplace_officer_group')[1]
    groups_ids = self.env.user.sudo().groups_id.ids
    if seller_group in groups_ids:
        login_ids = []
        if officer_group not in groups_ids:
            login_ids.append(self.env.user.sudo().partner_id.id)
        else:
            obj = self.env['res.partner'].search([('seller','=',True)])
            login_ids.extend(rec.id for rec in obj)
        return login_ids

class WebsiteCollectionalPage(models.Model):
    _inherit = 'website.collectional.page'

    @api.model
    def _set_seller_id(self):
        if self._context.get('mp_seller_collec_page'):
            user_obj = self.env['res.users'].sudo().browse(self._uid)
            if user_obj.partner_id and user_obj.partner_id.seller:
                return user_obj.partner_id.id
            return self.env['res.partner']

    marketplace_seller_id = fields.Many2one("res.partner", string="Seller", default=_set_seller_id, copy=False)

    template_ids = fields.Many2many('product.template', 'collectional_id', 'product_tmpl_id', 'coll_product_rel',
        string='Products',
        help="Add products on which this collection",
        domain = lambda self: [('marketplace_seller_id','in',compute_login_userid(self)),('marketplace_seller_id','!=',False),('status','=','approved'),('sale_ok','=',True),('website_published','=',True)] if self._context.get('mp_seller_collec_page') else [('sale_ok','=',True),('website_published','=',True)],
        )

    def get_all_products(self):
        try:
            condition = [('sale_ok', '=', True), ("website_published", "=", True)]
            if self.condition_match == "or":
                for _ in range(len(self.product_condition_ids) - 1):
                    condition.append("|")
            for obj in self.product_condition_ids:
                left_value = obj.field
                operator = obj.operator.operator
                if obj.field and obj.field == "type":
                    new_value = obj.value.strip().lower() if obj.value else ""
                    if "consu" in new_value:
                        right_value = "consu"
                    elif "stock" in new_value:
                        right_value = "product"
                    elif "serv" in new_value:
                        right_value = "service"
                    elif "digi" in new_value:
                        right_value = "digital"
                    else:
                        right_value = obj.value.strip() if obj.value else ""
                else:
                    right_value = obj.value.strip() if obj.value else ""
                if right_value:
                    right_value = str(right_value)
                condition.append((str(left_value), str(operator), right_value))
            if not condition:
                if self._context.get('mp_seller_collec_page'):
                    return self.env["product.template"].search([('marketplace_seller_id', '!=', False),('marketplace_seller_id.id','in',compute_login_userid(self)), ('status', '=', 'approved')])
                else:
                    return self.env["product.template"]

            if self._context.get('mp_seller_collec_page'):
                product_objs = self.env["product.template"].search(condition)
                product_objs = product_objs.filtered(lambda p: p.status == 'approved' and p.marketplace_seller_id.id in compute_login_userid(self))
            else:
                product_objs = self.env["product.template"].search(condition)
            return product_objs
        except:
            raise UserError(_("Entered value is not valid."))

class WebsiteCollectionalGroup(models.Model):
    _inherit = 'website.collectional.group'

    @api.model
    def _set_seller_id(self):
        user_obj = self.env['res.users'].sudo().browse(self._uid)
        if user_obj.partner_id and user_obj.partner_id.seller:
            return user_obj.partner_id.id
        return self.env['res.partner']

    marketplace_seller_id = fields.Many2one("res.partner", string="Seller", default=_set_seller_id, copy=False)
    collectional_page_ids = fields.Many2many('website.collectional.page', 'collectional_group_page_table', 'group_id', 'page_id', string='Collection Page', help="Add collection pages in this collection group", domain = lambda self: [('marketplace_seller_id','in',compute_login_userid(self)),('state','=','pub')] if self._context.get('mp_seller_collec_group') else [])

    @api.onchange('marketplace_seller_id')
    def _onchange_mp_seller_id(self):
        if self._context.get('mp_seller_collec_group') and self.collectional_page_ids:
            self.collectional_page_ids = False

class ProductCondition(models.Model):
    _inherit = 'product.condition'

    def _product_field_get(self):
        res = super(ProductCondition, self)._product_field_get()
        if self._context.get('mp_seller_collec_page'):
            if seller_ids := [item for item in res if 'seller_ids' in item]:
                res.remove(seller_ids[0])
        return res

    field = fields.Selection(_product_field_get, "Product Field", size=32,
        required=True, help="Associated field in the product form.")
