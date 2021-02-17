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

class LabTestUnit(models.Model):
    _name = 'patho.lab.testunit'
    _description = "Pathology Lab Test Units"
    _rec_name = 'code'

    name = fields.Char(string='Lab Test Unit')
    code = fields.Char('Code')
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide this record without removing it.")
