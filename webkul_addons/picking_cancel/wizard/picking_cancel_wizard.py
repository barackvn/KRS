# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import logging
import dateutil.parser
from datetime import datetime, timedelta

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class PickingCancelWizard(models.TransientModel):
    _name = "picking.cancel.wizard"
    _description = "Cancel Done Picking"

    reason_id = fields.Many2one('picking.cancel.reasons', string="Reason", required=True)
    reason = fields.Text(string='Comment', required=True)

    def cancel_done_picking(self):
        task_obj = self.env['stock.picking'].browse(self._context.get('active_id'))
        for record in [task_obj]:
            record.action_cancel()
            msg = "Reason for cancel the picking:- <b>%s</b><br/> <b>Comment:- </b> <br/>  %s" % (self.reason_id.name, self.reason)
            record.message_post(
                body=msg,
                subject=_('Stock Picking Cancel'),
                subtype='mail.mt_comment',
                partner_ids=record.message_partner_ids.ids
            )
        return True
