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


class TokenSession(models.Model):
    _name = 'token.session'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Token Session"
    _order = 'id desc'

    TOKEN_SESSION_STATE = [
        ('opening_control', 'Open'),
        ('opened', 'In Progress'),
        ('closing_control', 'Stopped'),
        ('closed', 'Closed'),
    ]

    name = fields.Char(
        string='Session ID', required=True, 
        readonly=True, default=lambda self: '/')
    config_id = fields.Many2one(
        'token.interface', string='Token Interface',
        help="The physical token interface you will use.",
        required=True,
        index=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible',
        required=True,
        index=True,
        readonly=True,
        states={'opening_control': [('readonly', False)]},
        default=lambda self: self.env.uid)
    start_at = fields.Datetime(string='Opening Date', readonly=True, copy=False)
    stop_at = fields.Datetime(string='Closing Date', readonly=True, copy=False)
    state = fields.Selection(
        TOKEN_SESSION_STATE, string='Status',
        required=True, readonly=True,
        index=True, copy=False, default='opening_control')

    @api.model
    def create(self, values):
        configId = values.get('config_id') or self.env.context.get('default_config_id')
        if not configId:
            raise UserError(_("You should assign a token interface to your session."))
        
        if self.search_count([
                ('state', '!=', 'closed'),
                ('config_id', '=', configId),
            ]) > 0:
            raise ValidationError(_("Another session is already opened for this interface."))

        tokenConfig = self.env['token.interface'].browse(configId)
        ctx = dict(self.env.context, company_id=tokenConfig.company_id.id)
        qsName = self.env['ir.sequence'].with_context(ctx).next_by_code('token.session')
        if values.get('name'):
            qsName += ' ' + values['name']
        values['name'] = qsName
        uid = SUPERUSER_ID if self.env.user.has_group('queue_management.group_queue_user') else self.env.user.id
        res = super(TokenSession, self.with_context(ctx).sudo(uid)).create(values)
        res.action_token_session_open()
        return res

    
    def action_token_session_open(self):
        # second browse because we need to refetch the data from the DB for cash_register_id
        # we only open sessions that haven't already been opened
        for session in self.filtered(lambda session: session.state == 'opening_control'):
            values = {}
            if not session.start_at:
                values['start_at'] = fields.Datetime.now()
            values['state'] = 'opened'
            session.write(values)
        return True

    
    def open_frontend_view(self):
        self.ensure_one()
        self.state = 'opened'
        return {
            'type': 'ir.actions.act_url',
            'url':   '/qms/web/session/{}'.format(self.id),
            'target': 'self',
            'session_id' : self.id
        }

    
    def action_session_closing_control(self):
        self.write({'state': 'closing_control', 'stop_at': fields.Datetime.now()})
        return True

    
    def action_session_close(self):
        self.write({'state': 'closed'})
        return {
            'type': 'ir.actions.client',
            'name': 'Queue Management Menu',
            'tag': 'reload',
            'params': {'menu_id': self.env.ref('queue_management.menu_token_interface').id},
        }
