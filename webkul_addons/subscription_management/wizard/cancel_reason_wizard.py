# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
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
##########################################################################


from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class CancelWizard(models.TransientModel):

    _name = "cancel.wizard"
    _description = "Wizard for getting Reason for cancel the subscription."

    @api.model
    def is_cancel_module(self):
        return self._context.get('is_cancel',False)


    is_cancel = fields.Boolean(string="Cancel", default=is_cancel_module)
    reason_id = fields.Many2one('subscription.reasons', string="Reason", required=True)
    comment = fields.Text(string="Comment")

    
    def get_cancel_subscription(self):
        subscription_obj = self.env['subscription.subscription'].browse(self._context.get('active_ids', []))
        if subscription_obj.get_cancel_sub():
            subscription_obj.reason = self.reason_id.name + self.comment if self.comment else ""
        return True


    
    def get_close_subscription(self):
        subscription_obj = self.env['subscription.subscription'].browse(self._context.get('active_ids', []))
        res = subscription_obj.reset_to_close()
        if res:
            subscription_obj.reason = self.reason_id.name + self.comment if self.comment else ""
        return res
