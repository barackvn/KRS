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
import logging
_logger=logging.getLogger(__name__)

class TestCriteria(models.Model):
    _name="patho.test.criteria"
    _description = "Pathology Test criteria"

    name = fields.Many2one('patho.test.parameters',required=True)
    unit = fields.Many2one(comodel_name="patho.lab.testunit" , string="Unit", related="name.unit", store=True)
    min_value = fields.Float(string="Minimum Value", related="name.min_value", store=True)
    max_value = fields.Float(string="Maximum Value", related="name.max_value", store=True)
    normal_value = fields.Float(string="Normal Value", related="name.normal_value", store=True)
    test_id = fields.Many2one('product.template', string="Test Id")
