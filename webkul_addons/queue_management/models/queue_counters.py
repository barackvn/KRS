# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError

import logging
_logger = logging.getLogger(__name__)


class QueueCounters(models.Model):
    _name = 'queue.counter'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Queue Counters"
    _order = 'id desc'


    def _get_group_queue_manager(self):
        return self.env.ref('queue_management.group_queue_manager')

    def _get_group_queue_user(self):
        return self.env.ref('queue_management.group_queue_user')


    name = fields.Char(string="Counter Name", required=True)
    active = fields.Boolean(default=True)
    session_ids = fields.One2many('queue.process', 'config_id', string='Sessions')
    current_session_id = fields.Many2one(
        'queue.process',
        compute='_compute_current_session',
        string="Current Session")
    current_session_state = fields.Char(compute='_compute_current_session')
    queue_session_username = fields.Char(compute='_compute_current_session_user')
    current_user_id = fields.Many2one('res.users')
    queue_session_state = fields.Char(compute='_compute_current_session_user')
    last_session_closing_date = fields.Date(compute='_compute_last_session')
    current_token = fields.Char(
        string='Current Token', readonly=True, copy=False, default='')
    current_token_day = fields.Datetime(
        string='Current Token Day', readonly=True, copy=False)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.user.company_id)
    group_queue_manager_id = fields.Many2one(
        'res.groups',
        string='QMS Manager Group',
        default=_get_group_queue_manager,
        help='This field is there to pass the id of the qms manager'
        ' group to the queue management system client.')
    group_queue_user_id = fields.Many2one(
        'res.groups',
        string='QMS User Group',
        default=_get_group_queue_user,
        help='This field is there to pass the id of the qms user'
        ' group to the queue management system client.')

    @api.depends('session_ids')
    def _compute_last_session(self):
        qSession = self.env['queue.process']
        for qConfig in self:
            session = qSession.search_read(
                [('config_id', '=', qConfig.id), ('state', '=', 'closed')],
                ['stop_at'],
                order="stop_at desc", limit=1)
            if session:
                qConfig.last_session_closing_date = session[0]['stop_at'].date()
            else:
                qConfig.last_session_closing_date = False

    @api.depends('session_ids')
    def _compute_current_session(self):
        for qConfig in self:
            session = qConfig.session_ids.filtered(lambda r: r.user_id.id == self.env.uid and \
                not r.state == 'closed')
            qConfig.current_session_id = session and session[0].id or False
            qConfig.current_session_state = session and session[0].state or False

    @api.depends('session_ids')
    def _compute_current_session_user(self):
        for qConfig in self:
            session = qConfig.session_ids.filtered(
                lambda s: s.state in ['opening_control', 'opened', 'closing_control'])
            qConfig.queue_session_username = session and session[0].user_id.name or False
            qConfig.queue_session_state = session and session[0].state or False


    
    def open_counter_dept_wiz(self):
        self.ensure_one()
        wizObj = self.env['qounter.department'].create({})
        ctx = dict(self._context or {})
        return {'name': "Select Department",
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'qounter.department',
                'res_id': wizObj.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'context': ctx,
                }

    @api.model
    def start_processing(self, deptId):
        ctx = dict(self._context or {})
        self = self.browse(ctx.get('active_id'))
        if not self.current_session_id:
            self.current_session_id = self.env['queue.process'].create({
                'user_id': self.env.uid,
                'config_id': ctx.get('active_id'),
                'dept_id': deptId,
            })
            self.current_session_id.state = 'opened'
            return self.start_queue_processing(self.current_session_id.id)
        return self.start_queue_processing(self.current_session_id.id)

    
    def start_queue_processing(self, qSessionId):
        self.ensure_one()
        self.current_session_id.state = 'opened'
        return {
            'type': 'ir.actions.act_url',
            'url': '/qms/web/processing/{}'.format(self.current_session_id.id),
            'target': 'self',
            'session_id': self.current_session_id.id
        }


    
    def open_new_session(self):
        """ new session button

        create one if none exist
        access cash control interface if enabled or start a session
        """
        self.ensure_one()
        if not self.current_session_id:
            self.current_session_id = self.env['queue.process'].create({
                'user_id': self.env.uid,
                'config_id': self.id
            })
            self.current_session_id.state = 'opened'
            return self.open_queue_session(self.current_session_id.id)
        return self.open_queue_session(self.current_session_id.id)

    
    def open_existing_queue_processing(self):
        """ close session button

        access session form to validate entries
        """
        self.ensure_one()
        if self.current_session_id.state == 'opening_control':
            self.current_session_id.state = 'opened'
        return self.open_queue_session(self.current_session_id.id)


    
    def open_session_view(self):
        self.ensure_one()
        return self.current_session_id.resume_session()

    def open_queue_session(self, sessionId):
        return {
            'name': _('Session'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'queue.process',
            'res_id': sessionId,
            'view_id': False,
            'type': 'ir.actions.act_window',
        }