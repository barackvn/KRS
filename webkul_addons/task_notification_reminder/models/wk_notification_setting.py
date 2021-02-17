# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################

import logging
from datetime import datetime, date, timedelta

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class TaskNotificationSetting(models.Model):
    _name = "task.notification.setting"
    _description = "For Notification Setting"

    name = fields.Char(string="Name", required=True)
    setting_for = fields.Selection([('deadline', 'Task Deadline')], string="Notification Setting For",
                                   required=True, default="deadline")
    project_ids = fields.Many2many("project.project", "project_notification",
                                   "notification_id", "project_id", string='Projects')
    task_ids = fields.Many2many('project.task', 'task_notification', 'notification_id', 'task_id',
        string='Task',
        help="If you don't select any task then this setting work \n for all the task based on project,"
             " and if project\n is also blank then work on all task assigned to you."
    )
    notification_deadline = fields.Selection(
        [('after', 'After'), ('before', 'Before'),
         ('after/before', 'After/Before')],
        required=True, default='before')
    notification_days = fields.Integer(string='Days', required=True)
    same_day = fields.Boolean(string='Same Day', default=True)
    enable_notification = fields.Boolean(string="Enable Mail Notification",
        help="It's a Boolean field, if its True the mail will send to the user who create the Notification."
    )
    project_manager = fields.Boolean(string="project Manager")
    task_followers = fields.Boolean(string="Task Followers")
    assigned_to = fields.Boolean(string="Assigned To", default=True)
    team_members = fields.Boolean(string="Team Members")
    is_active_notification = fields.Boolean(string="Active", default=True,
        help="Its a Boolean field, if it's True the notiifcation\n will create about the Task.")
    create_uid = fields.Many2one('res.users', 'Created By', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('assigned_to') or vals.get('project_manager') or vals.get('task_followers'):
            return super(TaskNotificationSetting, self).create(vals)
        else:
            raise UserError(_("You must Tick the Assigned to field."))

    def write(self, vals):
        res = super(TaskNotificationSetting, self).write(vals)
        for obj in self:
            if not (obj.assigned_to or obj.project_manager or obj.task_followers):
                raise UserError(_("You must choose atleast one of the nofification checkbox"
                                  " so that notification will send to you accordingly."))
        return res

    @api.onchange('project_ids')
    def _onchange_project_ids(self):
        lst = []
        task_ids = self.task_ids.ids
        self.task_ids = False
        for project_obj in self.project_ids:
            member_lst = []
            member_lst += project_obj.members.ids
            for follower_id in project_obj.message_partner_ids:
                if follower_id not in member_lst:
                    member_lst.append(follower_id.user_id.id)
            if project_obj.tasks:
                for task in project_obj.tasks:
                    if task.user_id.id == self._uid or project_obj.user_id.id == self._uid or self._uid in member_lst:
                        lst += task.ids
        self.task_ids = list(filter(lambda t: t in lst, task_ids))
        return {'domain': {'task_ids': [('id', 'in', lst)]}}

    def check_deadline(self, task_obj):
        today = date.today()
        if task_obj.date_deadline:
            d1 = task_obj.date_deadline
            if self.notification_deadline == 'before' or self.notification_deadline == 'after/before':
                if (d1 - today).days <= self.notification_days and (d1 - today).days > 0:
                    return True
            if self.notification_deadline == 'after' or self.notification_deadline == 'after/before':
                if (today - d1).days <= self.notification_days and (today - d1).days > 0:
                    return True
            if self.same_day:
                if (d1 - today).days == 0:
                    return True
        return False

    @api.model
    def send_mail_notification(self):
        setting = self.search([])
        today = date.today()
        _logger.info('============Deadline reminder mail======')
        if setting:
            for setting_obj in setting:
                task_ids_obj_lst = []
                if setting_obj.is_active_notification:
                    if setting_obj.project_ids and setting_obj.task_ids:
                        task_ids_obj_lst += setting_obj.task_ids
                    if setting_obj.task_ids:
                        if not setting_obj.project_ids:
                            task_ids_obj_lst += setting_obj.task_ids
                    if setting_obj.project_ids:
                        if not setting_obj.task_ids:
                            for project_id in setting_obj.project_ids:
                                task_ids_obj_lst += project_id.tasks
                    if not setting_obj.project_ids:
                        if not setting_obj.task_ids:
                            task_ids = self.env["project.task"].search(['|', '|',
                                ('user_id', '=', setting_obj.create_uid.id),
                                ('message_partner_ids', 'in', [setting_obj.create_uid.partner_id.id]),
                                ('project_id.user_id', '=', setting_obj.create_uid.id)
                            ])
                            for task_id in task_ids:
                                task_ids_obj_lst.append(task_id)
                    if task_ids_obj_lst:
                        for task_id in task_ids_obj_lst:
                            if task_id.stage_id and \
                                task_id.stage_id.name.lower() not in ["done", "cancel", 'cancelled']:
                                if task_id.date_deadline:
                                    result = setting_obj.check_deadline(task_id)
                                    if result:
                                        res = setting_obj.notification_send(task_id)
            return True

    def notification_send(self, task_id):
        rect_lst = []
        if self.project_manager:
            if task_id.project_id.user_id.id == self.create_uid.id:
                if task_id.project_id.user_id.partner_id.id not in rect_lst:
                    rect_lst.append(task_id.project_id.user_id.partner_id.id)
        if self.task_followers:
            if task_id.message_partner_ids:
                for follower_id in task_id.message_partner_ids:
                    if follower_id.id == self.create_uid.partner_id.id:
                        if follower_id.id not in rect_lst:
                            rect_lst.append(follower_id.id)
        if self.assigned_to:
            if task_id.user_id.id == self.create_uid.id:
                if task_id.user_id.partner_id.id not in rect_lst:
                    rect_lst.append(task_id.user_id.partner_id.id)
        if self.team_members:
            if task_id.project_id.members:
                for member in task_id.project_id.members:
                    if member.id == self.create_uid.id:
                        if member.partner_id.id not in rect_lst:
                            rect_lst.append(member.partner_id.id)
            if task_id.project_id.wk_team_id:
                if task_id.project_id.wk_team_id.members:
                    for team_member in task_id.project_id.wk_team_id.members:
                        if team_member.id == self.create_uid.id:
                            if team_member.partner_id.id not in rect_lst:
                                rect_lst.append(team_member.partner_id.id)
        return self.notification_create(task_id, rect_lst)

    def notification_create(self, task_obj, rect_lst):
        mail_id = False
        mail_id1 = False
        rec = self
        rec_lst = rect_lst
        today_date = date.today()
        today_start = datetime.strftime(datetime.now(), '%Y-%m-%d 00:00:00')
        today_end = datetime.strftime(datetime.now(), '%Y-%m-%d 23:59:59')
        yesterday = today_date + timedelta(days=-1)
        mail_message = self.env['mail.message']

        mail_message_ids = mail_message.search([('date', '<=', today_end),
                                                ('date', '>=', today_start),
                                                ('res_id', '=', task_obj.id),
                                                ('model', '=', 'project.task'),
                                                ('subject', '=', 'Task Deadline Notice')])
        for mail_message_obj in mail_message_ids:
            if mail_message_obj.partner_ids:
                for recipent_id in mail_message_obj.partner_ids:
                    if recipent_id.id in rec_lst:
                        rec_lst.remove(recipent_id.id)

        if rec_lst:
            template = self.env['ir.model.data'].xmlid_to_object(
                'task_notification_reminder.email_template_edi_wk_task_reminder'
            )
            if template:
                if self._context is None:
                    context = {}
                ctx = self._context.copy()
                ctx['notification_id'] = id
                ctx['email_to'] = [rec.create_uid.partner_id.id]
                mail_id = template.with_context(ctx).send_mail(task_obj.id, rec.enable_notification)
                if mail_id:
                    res = self.env['mail.mail'].browse(mail_id)
                    if res and res.mail_message_id:
                        res.mail_message_id.write({
                            'partner_ids': [(6, 0, rec_lst)],
                        })
                        for rec_id in rec_lst:
                            res.mail_message_id.write({
                                'notification_ids': [(0, 0, {
                                    'res_partner_id': rec_id,
                                    'notification_type': 'email',
                                    'notification_status': 'ready',
                                })],
                            })
                if not rec.enable_notification:
                    mail_id.cancel()
        return True


class Task(models.Model):
    _inherit = "project.task"

    def email_to(self):
        email_str = ''
        for obj in self:
            for user_id in self.env['res.partner'].browse(self._context.get('email_to')):
                if user_id.email:
                    email_str += user_id.email
                else:
                    for id in user_id.user_ids:
                        if id.email:
                            email_str += id.email
            return email_str
        return False
