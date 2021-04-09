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
import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    allow_prod_carousel = fields.Boolean("Allow Product Carousel")
    max_prod = fields.Integer("Maximum Number Of Products", help="Minimum number of products will be 3 for a perfect views\
        and maximum will be as defined in this field.", default=12)

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if vals.get("max_prod") and vals.get("max_prod")<3:
            raise UserError(_("Maximum Products must be atleast 3"))
        return res
