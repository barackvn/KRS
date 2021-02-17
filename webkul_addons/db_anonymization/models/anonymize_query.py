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
FIELD_STATES = [('clear', 'Clear'), ('random', 'Random'), ('fixed', 'Fixed Text')]

class AnnonymizeQuery(models.Model):
    _name = "anonymize.query"

    name = fields.Char(string="Query Name",required=True)
    database_query = fields.Text(string="Anonymize Query")
    active = fields.Boolean(String="Active",default=True)
    query_type = fields.Selection([("custom","Custom Query"),("raw","Raw Query")],default="custom",String="Query Type",required=1)
    # model_name = fields.Char('Object Name', )
    model_id = fields.Many2one('ir.model', string='Object', ondelete='set null')
    # field_name = fields.Char()
    field_id = fields.Many2one('ir.model.fields', string='Field', ondelete='set null')
    field_ttype = fields.Selection(related="field_id.ttype",readonly="1")
    state = fields.Selection(selection=FIELD_STATES, string='State', default='clear')
    fixed_text = fields.Char(string="Fixed Value")

    @api.onchange('model_id')
    def changeField_id(self):
        self.field_id = False
