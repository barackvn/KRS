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

class PathoSource(models.Model):
    _name = 'patho.source'
    _description = "Pathology TestRequest Source"

    name = fields.Char("Source", required=True)
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide this record without removing it.")
