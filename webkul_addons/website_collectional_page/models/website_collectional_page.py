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

from odoo import api, fields, models, _
from odoo import tools
from odoo import SUPERUSER_ID
from odoo.exceptions import Warning
from odoo.exceptions import UserError
import re
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)
from odoo.addons.website_webkul_addons.models.webkul_addons_config import WebkulWebsiteAddons

_operator = [
    ('in', "Contains"),
    ('not in', "Not Contains"),
    ('=', "Equal To"),
    ('! =', "Not Eqaul To"),
    ('<', "Is Less Than"),
    ('>', "Is Greater Than"),
    ('is set', "Is Set"),
    ('is not set', "Is Not Set")
]

_operator_for_boolean = [
    ('a', "Equal To"),
    ('b', "Not Eqaul To"),
]

product_field_type = []
product_selection_value = [('consu', _('Consumable')), ('service', _(
    'Service')), ('product', _('Stockable Product'))]


class WebsiteCollectionalPage(models.Model):
    _name = 'website.collectional.page'
    _description = "Website Collection Page"
    _inherit = ['website.published.mixin']

    @api.model
    def _get_page_title(self):
        return self.name

    @api.model
    def _get_page_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url = base_url + "/collections/"
        return (base_url)

    name = fields.Char(string='Title', help="", required=True)
    image = fields.Binary(string='Image', widget="image")
    template_ids = fields.Many2many('product.template', "collectional_table",
                                    "collectional_id", "product_id", string='Product Template')
    description = fields.Html(string='Description')
    website_published = fields.Boolean('Available in the website', copy=False)
    publish_date = fields.Datetime(string="Published Date")
    state = fields.Selection(
        [('pub', 'Published'), ('unpub', 'Unpublished')], string="State", default="unpub")
    # condition's Fields
    option = fields.Selection([("manually", "Manually select products"), ("conditionally",
                                                                          "Automatically select products based on conditions")], string="Option", default="manually")
    condition_match = fields.Selection(
        [("and", "All Conditions"), ("or", "Any Condition")], string="Products must match", default="and")
    product_condition_ids = fields.One2many(
        "product.condition", "collectional_id", string="Condition(s)")
    product_count = fields.Integer(
        string="Total Products:", compute="_count_product_template_ids")
    # SEO fields
    page_title = fields.Char(string="Meta title", default=_get_page_title)
    meta_description = fields.Char(string="Meta description", size=160)
    url = fields.Char(string="URL", default=_get_page_url)
    url_handler = fields.Char("Url Handler", required=True)

    _sql_constraints = [('url_handler_unique', 'unique(url_handler)',
                         'Url Handler must be unique for every collection !')]
    page_type = fields.Selection([('banner','Collection Banner Only'), ('product' , 'Collection Products')], string= 'Display On Website', default='banner', required=True)
    group_id = fields.Many2one('website.collectional.group', string="Collection Group")
    display_block = fields.Boolean(string="Display Block" , default=True)
    block_pos = fields.Selection([('left', 'Left'), ('right', 'Right')],string="Block Position", default="right")

    @api.depends('template_ids')
    def _count_product_template_ids(self):
        for rec in self:
            rec.product_count = len(rec.template_ids.ids)

    @api.onchange('description')
    def on_change_description(self):
        if self.description:
            meta_description = re.sub("<.*?>", " ", self.description or "")
            self.meta_description = meta_description.strip() or ""

    @api.onchange('name')
    def on_change_name(self):
        self.page_title = self.name or ""
        self.url_handler = self.name or ""

    @api.onchange('url_handler')
    def on_change_url_handler(self):
        self.url_handler = self.url_handler.replace(
            " ", "") if self.url_handler else ""
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url = base_url + "/collections/"
        self.url = base_url + (self.url_handler or "")

    @api.onchange('option')
    def on_change_option(self):
        self.template_ids = [(6, 0, [])]

    @api.onchange('product_condition_ids')
    def on_change_condition(self):
        if self.product_condition_ids:
            product_objs = self.get_all_products()
            self.template_ids = [(6, 0, product_objs.ids)]
        # Newly Added
        else:
            self.template_ids = False

    @api.onchange('condition_match')
    def on_change_condition_match(self):
        if self.id or self.product_condition_ids:
            product_objs = self.get_all_products()
            self.template_ids = [(6, 0, product_objs.ids)]

    @api.model
    def create(self, vals):
        if vals["option"] == "conditionally":
            product_objs = self.get_all_products()
            vals["template_ids"] = [(6, 0, product_objs.ids)]
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url = base_url + "/collections/"
        vals['url'] = base_url + (vals['url_handler'] or self.url_handler)
        res = super(WebsiteCollectionalPage, self).create(vals)
        return res

    def write(self, vals):
        res = super(WebsiteCollectionalPage, self).write(vals)
        for obj in self:
            curr_state = vals.get("state") if vals.get("state") else obj.state
            if curr_state == 'pub'and not obj.template_ids:
                obj.state = 'unpub'
            if curr_state == 'pub'and not obj.image:
                obj.state = 'unpub'
            vals.clear()
            if obj.option == "conditionally" and not vals.get("template_ids"):
                product_objs = obj.get_all_products()
                vals["template_ids"] = [(6, 0, product_objs.ids)]
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            base_url = base_url + "/collections/"
            vals['url'] = base_url + (vals.get("url_handler")
                                      and vals['url_handler'] or obj.url_handler)
            res = super(WebsiteCollectionalPage, obj).write(vals)
        return res

    def get_all_products(self):
        try:
            condition = [('sale_ok', '=', True), ("website_published", "=", True)]
            if self.condition_match == "or":
                for obj in range(len(self.product_condition_ids) - 1):
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
                return self.env["product.template"]
            product_objs = self.env["product.template"].search(condition)
            return product_objs
        except:
            raise UserError(_("Entered value is not valid."))

    def add_products_on_condition(self):
        self.ensure_one()
        product_objs = self.get_all_products()
        self.template_ids = [(6, False, product_objs.ids)]

    def remove_products_on_condition(self):
        self.ensure_one()
        if not len(self.template_ids):
            raise UserError("There is no product to remove.")
        self.template_ids = [(6, False, [])]

    def website_publish_button(self):
        if not self.template_ids:
            raise UserError(_("Please add some products to publish this Collection Page."))
        if not self.image:
            raise UserError('No banner added, please add a banner before publishing.')
        self.publish_date = datetime.today()
        self.state = "pub"

    def website_unpublish_button(self):
        self.publish_date = False
        self.state = "unpub"


class ProductCondition(models.Model):
    _name = 'product.condition'
    _description = "Product Condition"

    def _product_field_get(self):
        ids = self.env['ir.model.fields'].sudo().search([('model', 'in', ['product.template']), ('name', 'in', [
                                                 'name', 'type', 'seller_ids', 'list_price', 'public_categ_ids'])])
        res = []
        for field in ids:
            if not (field.name, field.field_description) in res:
                res.append((field.name, field.field_description))
            if not (field.name, field.ttype) in product_field_type:
                product_field_type.append((field.name, field.ttype))
        return res

    @api.onchange('field')
    def _product_field_type(self):
        ids = self.env['ir.model.fields'].sudo().search(
            [('model', 'in', ['product.template']), ('ttype', '=', 'boolean')])
        result = {}
        for field in ids:
            if not (field.name, field.ttype) in product_field_type:
                product_field_type.append((field.name, field.ttype))
            test = dict(product_field_type)

            if test.get(self.field):
                self.field_type = test[self.field]
                search_field = "wk_" + test[self.field]
                operator_obj = self.env["condition.operator"].search(
                    [(search_field, '=', True)])
                if operator_obj:
                    result['domain'] = {'operator': [
                        ('id', 'in', operator_obj.ids)]}
                else:
                    result['domain'] = {'operator': [('id', 'in', [])]}
            self.operator = False
            return result

    @api.model
    def get_reference_type(self):
        if self.field_type == "boolean":
            return _operator_for_boolean
        else:
            return _operator

    name = fields.Char("Condition Name", translate=True)
    collectional_id = fields.Many2one(
        "website.collectional.page", string="Collection Page")
    active = fields.Boolean("Active", default=True)
    field = fields.Selection(_product_field_get, "Product Field", size=32,
                             required=True, help="Associated field in the product form.")
    field_type = fields.Char("Field Type", default="None")
    operator = fields.Many2one(
        'condition.operator', string="Operator", required=True)
    value = fields.Char("Value", required=True)

class ConditionalOperator(models.Model):
    _name = 'condition.operator'
    _description = "Operator Wil Use In Condition"

    name = fields.Char("Operator Name", required=True)
    operator = fields.Char("Symbol/Char", required=True)

    wk_many2one = fields.Boolean("Many2one")
    wk_many2many = fields.Boolean("Many2many")
    wk_one2many = fields.Boolean("one2many")
    wk_boolean = fields.Boolean("Boolean")
    wk_char = fields.Boolean("Char")
    wk_text = fields.Boolean("Text")
    wk_selection = fields.Boolean("Selection")
    wk_integer = fields.Boolean("Integer")
    wk_float = fields.Boolean("Float")
    wk_html = fields.Boolean("Html")


class WebsiteCollectionalGroup(models.Model):
    _name = 'website.collectional.group'
    _description = "Website Collection Group"

    name =fields.Char(string='Name', required=True)
    group_type = fields.Selection([('carousel','Single Collection Carousel'), ('simple' , 'Multi Collection Carousel')],
        string= 'Display on website', default='carousel', required=True)
    collectional_page_ids = fields.Many2many('website.collectional.page', 'collectional_group_page_table', 'group_id', 'page_id',
        string='Collection Page')
    published_date = fields.Datetime(string="Published Date")
    state = fields.Selection([('published', 'Published'), ('unpublished', 'Unpublished')], string="State", default="unpublished")

    @api.model
    def create(self, vals):
        if not vals.get('collectional_page_ids'):
            raise UserError(_("Please add atleast one collection."))
        res= super(WebsiteCollectionalGroup, self).create(vals)
        return res

    def website_published_button(self):
        if not self.collectional_page_ids:
            raise UserError(_("Please add atleast one collection page."))
        if self.collectional_page_ids and self.collectional_page_ids.filtered(lambda p:p.image == None):
            raise UserError(_("Banner id not added in all the collection page added in this group.Please add banner first."))
        self.published_date = datetime.today()
        self.state = "published"

    def website_unpublished_button(self):
        self.published_date = False
        self.state = "unpublished"
