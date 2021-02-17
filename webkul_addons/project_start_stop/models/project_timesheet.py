# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import logging
import math
import time
import pytz
from datetime import date, datetime, timedelta

from odoo import api, fields, models
from odoo import tools, _
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

def float_time_convert(float_val):
    """convert float to float_time so visible in front end."""
    factor = float_val < 0 and -1 or 1
    val = abs(float_val)
    hours = factor * int(math.floor(val))
    minutes = int(round((val % 1) * 60))
    return ("%s H: %s M" % (str(hours).zfill(2), str(minutes).zfill(2)))

class AccountAnalyticLine(models.Model):
    """ Provide basics features for time tracking."""
    _inherit = 'account.analytic.line'
    _order = 'id desc'

    @api.model
    def _work_log_name(self):
        res = []
        res.append(("task.work.log", "Project Task Work Log"))
        return res

    type = fields.Selection('_work_log_name', "Name")
    start_time = fields.Datetime(string="Start Time")
    stop_time = fields.Datetime(string="Stop Time")
    last_update = fields.Date(compute="_last_update_date", string="Last Update Date", store=True)
    create_date = fields.Datetime("Creation Date", readonly=1)
    write_date = fields.Datetime("Update Date", readonly=1)
    hours = fields.Char(compute="_get_hours", string="Hours")
    user_id = fields.Many2one("res.users", string="User")
    is_log_active = fields.Boolean(string="Active", default=False)
    last_log_id = fields.Integer(string="Time Log Id")
    task_id = fields.Many2one("project.task", string="Task")

    @api.depends("create_date")
    def _last_update_date(self):
        """ Function for computed field 'last_update'."""
        for obj in self:
            obj.last_update = obj.create_date.date()

    def _get_hours(self):
        """ Function for computed field 'hours'. Calculate hours between two time duration"""
        for obj in self:
            if obj.stop_time and obj.start_time:
                worked_time = obj.stop_time - obj.start_time
                worked_time_seconds = worked_time.total_seconds()/3600.0
                obj.hours = float_time_convert(worked_time_seconds)
            else:
                obj.hours = float_time_convert(0)

    def return_wizard(self, vals):
        wizard_id = self.env['work.log.wizard'].create(vals)
        return {
            'name' : _("Warning"),
            'view_mode' : 'form',
            'view_id' : self.env['ir.model.data'].xmlid_to_object('project_start_stop.active_work_log_message_wizard').id,
            'res_model' : 'work.log.wizard',
            'res_id' : wizard_id.id,
            'type' : 'ir.actions.act_window',
            'nodestroy' : True,
            'target' : 'new',
            'domain' : '[]',
        }

    def check_allowed_user(self, obj):
        """ This function is design to check whether the employee working on other task, employee can work only on one task at a time."""
        if obj and (not obj.user_id or self._uid not in [obj.user_id.id]):
            vals = {'task_id': obj.id}
            return self.return_wizard(vals)
        return False

    def check_current_work(self):
        """ This function is design to check whether the employee working on other task, employee can work only on one task at a time."""
        #Find active work log for this user
        active_work_log_obj = self.env["account.analytic.line"].search([
            ('user_id', '=', self._uid),
            ('is_log_active', '=', True)], limit=1)
        if active_work_log_obj:
            vals = {}
            if active_work_log_obj.task_id:
                vals = {
                    'task_work_log_id': active_work_log_obj.id,
                    'task_name': active_work_log_obj.task_id.name,
                    'task_id': active_work_log_obj.task_id.id
                }
            return self.return_wizard(vals)
        return False

    def check_all_info_for_log(self, obj):
        res = {}
        if obj:
            for o in obj:
                wizard = self.check_allowed_user(obj=o)
                if wizard:
                    res.update({"wizard": wizard})
                    return res
                wizard2 = self.check_current_work()
                if wizard2:
                    res.update({"wizard": wizard2})
                    return res
                if o.log_action != "not_working":
                    raise ValidationError(_('You can not start "%s" because this task has been already closed. You need to reactivate it first.')%o.name)
                res.update({"can_start" : True})
        return res

    def work_log_start(self, obj):
        if obj:
            try:
                vals = {
                    'user_id' : self._uid,
                    'start_time' : datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                    'is_log_active' : True,
                    'task_id': obj.id,
                    'account_id' : obj.project_id.analytic_account_id.id if obj.project_id and obj.project_id.analytic_account_id else False,
                    'name' : "Working...",
                    'project_id' : obj.project_id.id if obj.project_id else False,
                    'create_uid' : self._uid,
                }
                work_log_obj = self.create(vals)
                work_log_obj.write({'last_log_id': work_log_obj.id})
                obj.write({
                    "log_action": 'working',
                    "last_start_time": work_log_obj.start_time
                })
                return work_log_obj
            except Exception as e:
                if not obj.project_id:
                    raise UserError(_("Task which you are going to start has no project. So you can't start working on task now. Assign project first then try again. "))
                else:
                    raise UserError(_("You are not authorized to read associated project. So contact your team leader to add you as team memebr to associated project then try again."))
        return False

    def work_log_stop(self, objs):
        """ Function to stop work time log."""
        for obj in objs:
            if not self.check_allowed_user(obj=obj):
                task_work_log_obj = self.search([("task_id","=",obj.id),("is_log_active","=",True)])
                if task_work_log_obj:
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    stop_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
                    start_time = task_work_log_obj.start_time
                    total_spent_hours = (stop_time - start_time).total_seconds() / 3600.0
                    task_work_log_obj.write({
                        'stop_time': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                        'is_log_active': False,
                        "name": task_work_log_obj.wk_name_get(),
                        "unit_amount": total_spent_hours,
                    })
                    obj.write({"log_action":'not_working'})
                    return True
                else:
                    raise UserError(_('You need to start first.'))

    def wk_name_get(self):
        result = []
        for log in self:
            if not log.stop_time:
                user_tz = self._context.get("tz", 'Asia/Kolkata') or 'Asia/Kolkata'
                local = pytz.timezone(user_tz)
                date_start = datetime.strftime(pytz.utc.localize(log.start_time).astimezone(local),'%d-%m-%Y')
                date_stop = datetime.strftime(pytz.utc.localize(datetime.today()).astimezone(local),"%d-%m-%Y")
                if date_start == date_stop:
                    name = "Worked on %s (%s To %s)"%(
                        datetime.strftime(pytz.utc.localize(log.start_time).astimezone(local),'%d-%B-%Y'),
                        datetime.strftime(pytz.utc.localize(log.start_time).astimezone(local),"%H:%M:%S"),
                        datetime.strftime(pytz.utc.localize(datetime.today()).astimezone(local),"%H:%M:%S")
                    )
                    return name
                else:
                    name = "Worked on (%s To %s)"%(
                        datetime.strftime(pytz.utc.localize(log.start_time).astimezone(local),"%d-%B-%Y %H:%M:%S"),
                        datetime.strftime(pytz.utc.localize(datetime.today()).astimezone(local),"%d-%B-%Y %H:%M:%S")
                    )
                    return name
            else:
                return log.name

    def task_start(self, tasks):
        """ Function to start task time log."""
        for task_obj in tasks:
            res = self.check_all_info_for_log(obj=task_obj)
            if res.get("can_start"):
                return self.work_log_start(task_obj)
            else:
                return res.get("wizard")
        return False

    def task_stop(self,tasks):
        """ Function to stop task time log."""
        for task_obj in tasks:
            res = self.check_allowed_user(obj=task_obj)
            if not res:
                return self.work_log_stop(task_obj)
            else:
                return res

    def get_task_time_duration(self, task_ids):
        """ This function calculates the total time spent by employee(s) on the particular task."""
        context = self._context.copy() or {}
        for task_obj in self.env['project.task'].browse(task_ids):
            task_work_log_objs = self.search([('task_id', '=', task_obj.id)])
            message = ""
            log_user_ids = []
            time_report = {}
            if task_work_log_objs :
                worked_time_seconds = 0.0
                for obj in task_work_log_objs:
                    if obj.stop_time and obj.start_time:
                        worked_time = obj.stop_time - obj.start_time
                        worked_time_seconds += worked_time.total_seconds()
                    if obj.user_id.id not in log_user_ids:
                        log_user_ids.append(obj.user_id.id)
                worked_time_seconds = worked_time_seconds / 3600.0
                message = float_time_convert(worked_time_seconds)
                for user_id in log_user_ids:
                    log_obj = self.search([("task_id", "=", task_obj.id), ("user_id", "=", user_id)])
                    msg = ""
                    worked_time_seconds = 0.0
                    for obj in log_obj:
                        if obj.stop_time and obj.start_time:
                            worked_time = obj.stop_time - obj.start_time
                            worked_time_seconds += worked_time.total_seconds()
                    worked_time_seconds = worked_time_seconds / 3600.0
                    msg = float_time_convert(worked_time_seconds)
                    time_report.update({user_id : msg})
            context['time_report'] = time_report
            wizard_id = self.with_context(
                context).env['work.log.time.wizard'].create({
                    'task_id': task_ids[0],
                    'total_time': message
                })
            return {
                'name' : _("Time Log Report"),
                'view_mode' : 'form',
                'view_id' : self.env['ir.model.data'].xmlid_to_object('project_start_stop.work_total_hours_message_wizard').id,
                'res_model' : 'work.log.time.wizard',
                'res_id' : wizard_id.id,
                'type' : 'ir.actions.act_window',
                'nodestroy' : True,
                'target' : 'new',
                'domain' : '[]',
                'context': context,
            }
