# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################

from datetime import datetime, timedelta
import time

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class QueueProcess(models.Model):
    _name = 'queue.process'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Queue Process"
    _order = 'id desc'

    QUEUE_SESSION_STATE = [
        ('opening_control', 'Open'),
        ('opened', 'In Progress'),
        ('closing_control', 'Stopped'),
        ('closed', 'Closed'),
    ]

    name = fields.Char(
        string='Session ID', required=True, 
        readonly=True, default=lambda self: '/')
    config_id = fields.Many2one(
        'queue.counter', string='Queue Counter',
        help="The physical queue counter you will use.",
        required=True,
        readonly=True,
        states={'opening_control': [('readonly', False)]},
        index=True)
    dept_id = fields.Many2one(
        "department.department",
        readonly="True",
        states={'opening_control': [('readonly', False)]},
        string="Department")
    user_id = fields.Many2one(
        'res.users', string='Responsible',
        required=True,
        index=True,
        readonly=True,
        states={'opening_control': [('readonly', False)]},
        default=lambda self: self.env.uid)
    start_at = fields.Datetime(string='Opening Date', readonly=True, copy=False)
    stop_at = fields.Datetime(string='Closing Date', readonly=True, copy=False)
    next_token = fields.Char(
        string='Next Token', readonly=True, copy=False, default='')
    state = fields.Selection(
        QUEUE_SESSION_STATE, string='Status',
        required=True, readonly=True,
        index=True, copy=False, default='opening_control')

    @api.model
    def create(self, values):
        configId = values.get('config_id') or self.env.context.get('default_config_id')
        if not configId:
            raise UserError(_("You should assign a queue counter to your session."))
        
        if self.search_count([
                ('state', '!=', 'closed'),
                ('config_id', '=', configId),
            ]) > 0:
            raise ValidationError(_("Another session is already opened for this counter."))

        queueCounter = self.env['queue.counter'].browse(configId)
        ctx = dict(self.env.context, company_id=queueCounter.company_id.id)
        qsName = self.env['ir.sequence'].with_context(ctx).next_by_code('queue.process')
        if values.get('name'):
            qsName += ' ' + values['name']
        values['name'] = qsName
        uid = SUPERUSER_ID if self.env.user.has_group('queue_management.group_queue_user') else self.env.user.id
        res = super(QueueProcess, self.with_context(ctx)).create(values)
        res.action_queue_process_open()
        queueCounter.current_user_id = self.env.user.id
        return res

    
    def action_queue_process_open(self):
        for session in self.filtered(lambda session: session.state == 'opening_control'):
            values = {}
            if not session.start_at:
                values['start_at'] = fields.Datetime.now()
            values['state'] = 'opened'
            session.write(values)
        return True

    @api.model
    def start_time(self):
        zoneSecs = time.timezone
        timeNow = datetime.now()
        midNight = timeNow.replace(hour=0, minute=0, second=0, microsecond=0)
        if zoneSecs > 0:
            timeFrom = str(midNight + timedelta(0, zoneSecs))
        else:
            zoneSecs = -zoneSecs
            timeFrom = str(midNight - timedelta(0, zoneSecs))
        return timeFrom

    
    def get_next_token(self):
        self.ensure_one()
        newToken = self.next_token
        tokenModel = self.env['token.token']
        timeFrom = self.start_time()
        domain = [('state', 'not in', ['draft', 'cancel']), ('date', '>=', timeFrom)]
        if not newToken:
            tokenNo = tokenModel.search(domain).mapped('token_day_number')
            if tokenNo:
                tokenNo = sorted(tokenNo)
                newToken = str((int(tokenNo[-1]) + 1)).zfill(3)
            else:
                newToken = '001'
        domain[0] = ('state', '=', 'draft')
        domain.append(('token_day_number' ,'=', newToken))
        nextToken = tokenModel.search(domain)
        if nextToken:
            self.next_token = str((int(newToken) + 1)).zfill(3)
            nextToken.write({
                'state' : 'progress',
                'process_by' : self.env.uid,
                'queue_session' : self.id,
            })
            return {
                'name': _('Session'),
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'token.token',
                'res_id': nextToken.id,
                'view_id': False,
                'type': 'ir.actions.act_window',
            }
        self.next_token = ''
        displayMessage = "Token queue is empty!"
        return self.display_message(displayMessage)

    def display_message(self, message):
        wizardObj = self.env['queue.message.wizard'].create({'text': message})
        return {
            'name': ("Information"),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'queue.message.wizard',
            'view_id': self.env.ref('queue_management.qms_wizard_view').id,
            'res_id': wizardObj.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
        }

    
    def action_session_closing_control(self):
        self.write({
            'state': 'closing_control',
            'stop_at': fields.Datetime.now()
        })
        return True

    
    def resume_session(self):
        self.ensure_one()
        self.state = 'opened'
        return {
            'type': 'ir.actions.act_url',
            'url': '/qms/web/processing/{}'.format(self.id),
            'target': 'self',
            'session_id': self.id
        }

    
    def action_session_close(self):
        self.write({'state': 'closed'})
        self.config_id.current_user_id = False
        return {
            'type': 'ir.actions.client',
            'name': 'Queue Management Menu',
            'tag': 'reload',
            'params': {'menu_id': self.env.ref('queue_management.menu_queue_counters').id},
        }