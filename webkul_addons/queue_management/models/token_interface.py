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


class TokenInterface(models.Model):
    _name = 'token.interface'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Token Interface"
    _order = 'id desc'

    def _get_group_queue_manager(self):
        return self.env.ref('queue_management.group_queue_manager')

    def _get_group_queue_user(self):
        return self.env.ref('queue_management.group_queue_user')

    
    def _get_default_sequence(self):
        return self.env['token.sequence'].search([], limit=1).id

    name = fields.Char(string="Name")
    token_seq = fields.Many2one(
        'token.sequence',
        default=_get_default_sequence,
        required=True,
        string="Sequence Ref #",
        help="Token ref for this token interface will generate as per selected sequence"
    )
    # partner_id = fields.Many2one('res.partner', string="User")
    active = fields.Boolean(default=True)
    session_ids = fields.One2many('token.session', 'config_id', string='Sessions')
    current_session_id = fields.Many2one(
        'token.session',
        compute='_compute_current_session',
        string="Current Session")
    current_session_state = fields.Char(compute='_compute_current_session')
    token_session_username = fields.Char(compute='_compute_current_session_user')
    token_session_state = fields.Char(compute='_compute_current_session_user')
    last_session_closing_date = fields.Date(compute='_compute_last_session')
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

    use_posbox = fields.Boolean(string="PosBox")
    proxy_ip_addr = fields.Char(string='IP Address', size=45,
        help='The hostname or ip address of the hardware proxy')

    @api.depends('session_ids')
    def _compute_last_session(self):
        TokenSession = self.env['token.session']
        for tokenConfig in self:
            session = TokenSession.search_read(
                [('config_id', '=', tokenConfig.id), ('state', '=', 'closed')],
                ['stop_at'],
                order="stop_at desc", limit=1)
            if session:
                tokenConfig.last_session_closing_date = session[0]['stop_at'].date()
            else:
                tokenConfig.last_session_closing_date = False

    @api.depends('session_ids')
    def _compute_current_session(self):
        for tokenConfig in self:
            session = tokenConfig.session_ids.filtered(lambda r: r.user_id.id == self.env.uid and \
                not r.state == 'closed')
            # sessions ordered by id desc
            tokenConfig.current_session_id = session and session[0].id or False
            tokenConfig.current_session_state = session and session[0].state or False

    @api.depends('session_ids')
    def _compute_current_session_user(self):
        for tokenConfig in self:
            session = tokenConfig.session_ids.filtered(
                lambda s: s.state in ['opening_control', 'opened', 'closing_control'])
            tokenConfig.token_session_username = session and session[0].user_id.name or False
            tokenConfig.token_session_state = session and session[0].state or False

    
    def open_new_session(self):
        """ new session button

        create one if none exist
        access control interface if enabled or start a session
        """
        self.ensure_one()
        if not self.current_session_id:
            self.current_session_id = self.env['token.session'].create({
                'user_id': self.env.uid,
                'config_id': self.id
            })
        return self.resume_open_session()
        # return self._open_session_qms(self.current_session_id.id)

    
    def resume_open_session(self):
        self.ensure_one()
        self.current_session_id.state = 'opened'
        return {
            'type': 'ir.actions.act_url',
            'url': '/qms/web/session/{}'.format(self.current_session_id.id),
            'target': 'self',
            'session_id': self.current_session_id.id
        }

    
    def open_existing_session_qms(self):
        """ close session button

        access session form to validate entries
        """
        self.ensure_one()
        if self.current_session_id.state in ['opening_control', 'opened']:
            return self.resume_open_session()
        return self._open_session_qms(self.current_session_id.id)

    def _open_session_qms(self, sessionId):
        return {
            'name': _('Session'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'token.session',
            'res_id': sessionId,
            'view_id': False,
            'type': 'ir.actions.act_window',
        }
