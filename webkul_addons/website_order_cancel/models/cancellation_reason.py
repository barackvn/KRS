# -*- coding: utf-8 -*-
##########################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
##########################################################################
from odoo import models, fields, api, _


class OrderCancelReason(models.Model):
    _name = "order.cancel.reason"
    _order = "sequence asc"
    _description = "Order Cancel Reason"

    name = fields.Text(string="Name", required=True)
    sequence = fields.Integer(string="Sequence", required=True,)
    active = fields.Boolean(string="Active", default=True)
