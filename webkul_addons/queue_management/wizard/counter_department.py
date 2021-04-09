# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################


from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class QounterDepartment(models.TransientModel):
    _name = "qounter.department"

    counter_dept = fields.Many2one('department.department', string="Department")

    def start_processing(self):
        return self.env['queue.counter'].start_processing(self.counter_dept.id)
