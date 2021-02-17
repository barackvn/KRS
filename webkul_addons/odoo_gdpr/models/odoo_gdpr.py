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
class OdooGdpr(models.Model):
    _name = "odoo.gdpr"

    name = fields.Char(string="Name",required=True)
    gdpr_title = fields.Char(string="GDPR Statement Title",required=True, translate=True)
    title_info = fields.Html(String="GDPR Statement Description", translate=True,required=True)
    modal_desc = fields.Html(String="Message Before Removing Data", translate=True,required=True)
    # request_message = fields.Text(String="Default Request Message", translate=True,required=True)
    allow_gdpr_message = fields.Boolean(String="Display GDPR Message on your Site's footer", default=True, help="Display a message on website homepage will know about GDPR european Law.")
    gdpr_message = fields.Text(String="GDPR Message", translate=True)
    download_request = fields.Selection([('done', "Auto Aproove"), ("pending", "Manual Aproove")], String="Download Request", default="pending")
    delete_request = fields.Selection([('done', "Auto Aproove"), ("pending", "Manual Aproove")], String="Delete Request",default="pending")

    # gdpr_data_tmpl_id = fields.One2many('gdpr.data.template','gdpr_id', String="Gdpr Data Template")
