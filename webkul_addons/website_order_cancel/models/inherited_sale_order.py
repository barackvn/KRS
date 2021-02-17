# -*- coding: utf-8 -*-
##########################################################################
#
#	Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
from odoo import models, fields, api, _
from odoo import SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    reason_id = fields.Many2one(
        'order.cancel.reason', string="Cancellation Reason")
    additional_remark = fields.Text(string='Additional Remark')
