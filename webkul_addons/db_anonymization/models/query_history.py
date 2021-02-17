# -*- coding: utf-8 -*-
#################################################################################
# Author : Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>;
#################################################################################
from odoo import models, fields,api,_
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError

class QueryHistory(models.Model):
    _name = "query.history"

    anonymize_query_id = fields.Many2one('anonymize.query',string='Anonymize Query' ,readonly=True)
    database_backup_id = fields.Many2one('database.backup',string='Clone Database',readonly=True)
    query_response = fields.Text(string="Query Response",readonly=True)
