# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import logging
from odoo import fields, models

_logger = logging.getLogger(__name__)


class PickingCancelReasons(models.Model):
    _name = "picking.cancel.reasons"
    _description = "Picking Cancel Reasons"
    _order = "sequence asc"

    name = fields.Char(string="Reason", required=True)
    sequence = fields.Integer(string="Sequence", required=True)
