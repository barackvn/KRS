# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import logging

from odoo import api, fields, models
from odoo import tools, _

_logger = logging.getLogger(__name__)


class WorkLogWizard(models.TransientModel):
    _name = "work.log.wizard"
    _description = "Wizard For Work Log"

    def _set_message(self):
        for obj in self:
            if obj.task_name:
                obj.message = "You are currently working on " + obj.task_name + " task."

    task_work_log_id = fields.Many2one("account.analytic.line", string="Task Work Log")
    task_id = fields.Many2one("project.task", "Task")
    task_name = fields.Char(string="Task Name", help="Task Name")
    message = fields.Char(compute="_set_message", string='Week No')

    def countinue(self):
        for obj in self:
            if obj.task_work_log_id:
                obj.task_work_log_id.task_id.task_stop()
            if self._context.get('active_model') == 'project.task':
                if self._context.get('active_id') :
                    task = self.env["project.task"].browse(self._context.get('active_id'))
                    self.env["account.analytic.line"].task_start(task)
        return {
                'type': 'ir.actions.client',
                'tag': 'reload',
        }

class WorkLogTimeWizard(models.TransientModel):
    _name = "work.log.time.wizard"
    _description = "Wizard For Work Log"

    @api.model
    def _set_task_id(self):
        if self._context.get('active_model') == 'project.task':
            return self._context.get('active_id')
        else :
            return False

    task_id = fields.Many2one("project.task", string="Task")
    total_time = fields.Char(string="Total time spent")
    total_time_report = fields.Html(string="Time Log Report")

    @api.model
    def default_get(self, fields):
        res = super(WorkLogTimeWizard, self).default_get(fields)
        if self._context.get('time_report'):
            time_report = self._context.get('time_report')
            message = "<table style='width:100%;background-color: #fff;border-collapse: separate;'>" \
                      "<tr style='background-color: #36364B;color: white;'>" \
                      "<th style='text-align:center;padding: 5px;'>S.no </th>" \
                      "<th style='text-align:center;padding: 5px;'> Employee </th>" \
                      "<th style='text-align:center;padding: 5px;'> Spent Time </th>" \
                      "</tr>"
            count=1
            for key in time_report.keys():
                user_obj = self.env["res.users"].browse(key)
                message += "<tr>" \
                           "<td style='text-align:center; background-color: #eee;'> %s.</td>" \
                           "<td style='text-align:center; background-color: #eee;'>%s</td>" \
                           "<td style='text-align:center; background-color: #eee;text-align:center;'>%s</td>" \
                           "</tr>" % (count, user_obj.name, time_report[key])
                count += 1
            message += "</table>"
            res['total_time_report'] = message
        return res
