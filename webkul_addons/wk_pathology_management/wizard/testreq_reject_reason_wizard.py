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
_logger = logging.getLogger(__name__)

class TestReqRejectReason(models.TransientModel):
    _name="testreq.rejectreason.wizard"
    _description = "Pathology Reject Reason"

    add_reason = fields.Text(string="Reason for Rejection")

    
    def button_addreason(self):
        obj = self.env['patho.testrequest'].browse(self._context.get('active_ids'))
        reason_msg = ''
        if obj:
            reason_msg = "Reason for Rejection of TestRequest : " + self.add_reason
            obj.message_post(body=reason_msg)
            obj.write({'status' : 'rejected'})
