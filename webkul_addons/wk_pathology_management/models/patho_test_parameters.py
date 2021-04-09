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

from odoo import models,fields
from odoo.tools.translate import html_translate
import logging
_logger=logging.getLogger(__name__)

class TestParameters(models.Model):
    _name="patho.test.parameters"
    _description = "Pathology Test Parameters"

    name = fields.Char("Parameter",required=True)
    sequence = fields.Integer("Sequence")
    unit = fields.Many2one(comodel_name="patho.lab.testunit" , string="Unit")
    min_value = fields.Float(string="Minimum Value",required=True)
    max_value = fields.Float(string="Maximum Value",required=True)
    normal_value = fields.Float(string="Normal Value",required=True)
    description = fields.Html('Description', translate=html_translate, sanitize=False)
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide this record without removing it.")
