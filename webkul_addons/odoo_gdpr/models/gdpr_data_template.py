# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
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
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError
from odoo import models, fields,api,_
class GdprDataTemplate(models.Model):
    _name = "gdpr.data.template"

    name = fields.Char(string = "Name",required=True)
    icon = fields.Binary(string="Icon")
    # title = fields.Char(String="Title", translate=True)
    desc = fields.Text(String="Description", translate=True)
    small_desc = fields.Text(compute='_compressDesc', translate=True)
    allow_delete = fields.Boolean(String="Allow Delete", default=False)
    allow_download = fields.Boolean(String="Allow Download", default=False)
    type = fields.Selection([("user","User"),("address","Address")], String="Type")
    active = fields.Boolean(String="Active", default=True)
    redirect_url = fields.Char(String="Redirect Url")
    # gdpr_id = fields.Many2one('odoo.gdpr', string='Odoo Gdpr')

    # @api.multi
    def _compressDesc(self):
        for o in self:
            o.small_desc = f"{o.desc[:125]}..." if len(o.desc) > 125 else o.desc
