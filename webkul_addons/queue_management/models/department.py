# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)


class DepartmentDepartment(models.Model):
    _name = 'department.department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Department"
    _order = 'name desc'

    name = fields.Char("Department")
