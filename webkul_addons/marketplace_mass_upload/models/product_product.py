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
from odoo.http import request
import os,csv
import logging
_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    
    _inherit = 'product.product'

    def download_sample_variants_csv(self):
       return {
            'type':'ir.actions.act_url',
            "target":'self',
            "url":'/download/sample/csv/{}'.format(self._context['active_ids'])
        }


        