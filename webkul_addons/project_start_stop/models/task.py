# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import logging
import math
import time

from datetime import date, datetime, timedelta
from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Task(models.Model):
    """ Inherit project.task for providing additional feature to every task."""
    _inherit = "project.task"

    def _last_update_date(self):
        """ Function for computed field 'last_update'."""
        for obj in self:
            obj.last_update = obj.write_date.date()

    last_update = fields.Date(compute="_last_update_date", string='Updated Date', store=True)
    log_action = fields.Selection([("working", "Working"),
                                   ("not_working", "Not Working"),
                                   ("closed", "Closed")],
                                  string="Log Action", copy=False, default="not_working")
    last_start_time = fields.Datetime(string="Last Start Time", help="Shows latest work start time.")
    log_ids = fields.One2many("account.analytic.line", 'task_id', string="Logs")
    completion_date = fields.Datetime("Completion Time")

    def stop_all_task(self):
        if not self:
            obj = self.search([('user_id', '=', self._uid), ('log_action', '=', 'working')])
            obj.task_stop()
        return True

    def copy(self, default=None):
        res = super(Task, self).copy(default)
        if res.log_action:
            res.log_action = "not_working"
        return res

    def task_start(self):
        """ Function to start task time log."""
        res = self.env["account.analytic.line"].task_start(self)
        return res

    def task_stop(self):
        """ Function to stop task time log."""
        res = self.env["account.analytic.line"].task_stop(self)
        return res

    def get_task_time_duration(self):
        """ Function to calculate total time spent by employee on task."""
        res = self.env["account.analytic.line"].get_task_time_duration(self.ids)
        return res

    def open_work_log(self):
        mod_obj = self.env['ir.model.data']
        logs = self.mapped("log_ids")
        result = self.env.ref('project_start_stop.wk_task_work_log_action').read()[0]
        result['domain'] = [('id', 'in', logs.ids if logs else [])]
        return result

    def project_task_reevaluate(self):
        """ This function is overriding here for updating working status of the task when task will reactivate. Status will be Not working."""
        if self.env['res.users'].has_group('project.group_time_work_estimation_tasks'):
            res = super(Task, self).project_task_reevaluate()
            return res
        for task_obj in self:
            res = super(Task, task_obj).project_task_reevaluate()
            if task_obj.state == "open":
                task_obj.log_action = "not_working"
        return res

    def write(self, vals):
        for obj in self:
            if obj.log_action == "working" and vals.get('user_id'):
                raise UserError(_("Currently, this task is in working state. First stop the task and then assign to other user."))
            if vals.get("stage_id", False):
                stage_obj = self.env["project.task.type"].browse(vals.get("stage_id"))
                if stage_obj and stage_obj.name.lower() in ["done", "cancel", 'cancelled']:
                    if obj.log_action == "working":
                        obj.task_stop()
                    obj.log_action = "closed"
                elif obj.stage_id and obj.stage_id.name.lower() in ["done", "cancel", 'cancelled']:
                    obj.log_action = "not_working"
        return super(Task, self).write(vals)
