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

from odoo import models,fields,api,_
from odoo.exceptions import UserError
import logging
_logger=logging.getLogger(__name__)
from odoo.tools.translate import html_translate

class ProductProduct(models.Model):
    _inherit = "product.product"

    
    def patho_test_only_show_package(self):
        return True

class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_default_category_id(self):
        res = super(ProductTemplate, self)._get_default_category_id()
        if self._context.get('default_is_test') or self._context.get('default_is_test_package'):
            categ_id = self.env.ref('wk_pathology_management.patho_default_product_category')
            return categ_id
        else:
            return res

    categ_id = fields.Many2one(
        'product.category', 'Internal Category',
        change_default=True, default=_get_default_category_id,
        required=True, help="Select category for the current product")
    is_test_package = fields.Boolean( string = "Is a test package", help= "Check if product is a package.")
    is_test = fields.Boolean( string = "Is a test", help= "Check if product is a test.")
    report_delivery_time = fields.Integer('Report Delivery Time', default=1)
    report_delivery_time_unit = fields.Selection([('day', 'Day'), ('week', 'Week')], default="day")
    product_tmpl_ids = fields.Many2many('product.template', "package_id", "tmpl_id", "package_tmpl_rel", string="Lab Tests")
    test_criteria = fields.One2many('patho.test.criteria', "test_id", string="Test Criteria",auto_join=True, copy=True)
    # appoint_id = fields.Many2one('appointment')
    labtest_count = fields.Integer(" Total Lab Tests", compute="count_labtest_in_package")
    parameter_count = fields.Integer(" Total Parameters", compute="count_parameters_in_pack")
    test_preinfo = fields.Many2one('patho.test.preinfo', string="Pre-Information", help="Write the pre-requisites of this test for patient.")
    test_sampletype = fields.Many2one('patho.test.sampletype', string="Sample Type", help="Give the required sample type of this test by patient.")
    test_note = fields.Html("Test Note", translate=html_translate, sanitize=False)

    
    def patho_test_only_show_package(self):
        return True

    
    def count_labtest_in_package(self):
        self.labtest_count = len(self.product_tmpl_ids)
        return True

    
    def count_parameters_in_pack(self):
        self.parameters_count = len(self.test_criteria)
        return True

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        if vals.get('is_test'):
            if not vals.get('test_criteria'):
                raise UserError(
                    'No Parameters in this test. Add atleast one Parameter.')
        if vals.get('is_test_package'):
            if not vals.get('product_tmpl_ids') or not vals.get('product_tmpl_ids')[0][2]:
                raise UserError(_('No test in this package. Select atleast one Test.'))
        return res

    
    def write(self, vals):
        for rec in self:
            is_test = vals.get('is_test') if vals.get('is_test') else rec.is_test
            is_test_package = vals.get('is_test_package') if vals.get('is_test_package') else rec.is_test_package
            if is_test:
                test_criteria = vals.get("test_criteria") if vals.get('test_criteria') else rec.test_criteria
                if not test_criteria:
                    raise UserError(_('No Parameters in this test. Add atleast one Parameter.'))
            if is_test_package:
                product_tmpl_ids = vals.get('product_tmpl_ids')[0][2] if vals.get('product_tmpl_ids') else rec.product_tmpl_ids
                if not product_tmpl_ids:
                    raise UserError(_('No test in this package. Select atleast one Test.'))
        res = super(ProductTemplate, self).write(vals)
        return res

    @api.onchange('product_tmpl_ids')
    def compute_package_price(self):
        package_price = 0
        if self.is_test_package:
            if self.product_tmpl_ids:
                for test in self.product_tmpl_ids:
                    package_price = package_price + test.list_price
        self.list_price = package_price


class TestPreinfo(models.Model):
    _name = "patho.test.preinfo"
    _description = "Pathology Test PreInfo"

    name = fields.Char("Information", required=True)


class TestSampleType(models.Model):
    _name = "patho.test.sampletype"
    _description = "Pathology Test Sample Types"

    name = fields.Char("Sample Type", required=True)
