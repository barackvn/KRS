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


class TokenSequence(models.Model):
    _name = 'token.sequence'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Token Sequence"
    _order = 'id desc'


    name = fields.Char(string="Sequence Name", required=True)
    prefix = fields.Char(string='Short Code', size=5, 
        help="The token number of this this sequence will be named using this prefix.")
    padding = fields.Integer(string="Padding", required=True, default=4)
    number_increment = fields.Integer(string="Increment", required=True, default=1)
    sequence_id = fields.Many2one(
        'ir.sequence', string='Entry Sequence',
        readonly=True, copy=False,
        help="This field contains the information related to the numbering of \
        the token number of this sequence.")
    number_sequence_next = fields.Integer(string='Next Number',
        help='The next sequence number will be used for the next token.',
        compute='_compute_seq_number_next',
        inverse='_inverse_seq_number_next')
    company_id = fields.Many2one(
        'res.company', string='Company', 
        required=True, index=True, 
        default=lambda self: self.env.user.company_id,
        help="Company related to this token sequence")
    notes = fields.Text(string="Note", help="Sequence description")


    
    # do not depend on 'sequence_id.date_range_ids', because
    # sequence_id._get_current_sequence() may invalidate it!
    @api.depends('sequence_id.use_date_range', 'sequence_id.number_next_actual')
    def _compute_seq_number_next(self):
        '''Compute 'number_sequence_next' according to the current sequence in use,
        an ir.sequence or an ir.sequence.date_range.
        '''
        for token in self:
            if token.sequence_id:
                sequence = token.sequence_id._get_current_sequence()
                token.number_sequence_next = sequence.number_next_actual
            else:
                token.number_sequence_next = 1

    
    def _inverse_seq_number_next(self):
        '''Inverse 'number_sequence_next' to edit the current sequence next number.
        '''
        for token in self:
            if token.sequence_id and token.number_sequence_next:
                sequence = token.sequence_id._get_current_sequence()
                sequence.number_next = token.number_sequence_next

    @api.model
    def _get_sequence_prefix(self, code):
        prefix = '%(range_year)s/%(month)s/%(day)s/'
        if code:
            code = code.upper()
            prefix = code + '/' + prefix
        return prefix


    @api.model
    def _create_sequence(self, vals):
        """ Create new no_gap entry sequence for every new token sequence"""
        prefix = self._get_sequence_prefix(vals.get('prefix', ''))
        seq = {
            'name': vals['name'],
            'implementation': 'no_gap',
            'prefix': prefix,
            'padding': vals['padding'],
            'number_increment': vals['number_increment'],
            'use_date_range': True,
        }
        if 'company_id' in vals:
            seq['company_id'] = vals['company_id']
        seq = self.env['ir.sequence'].create(seq)
        seq_date_range = seq._get_current_sequence()
        seq_date_range.number_next = vals.get('number_sequence_next', 1)
        return seq


    @api.model
    def create(self, vals):
        if not vals.get('sequence_id'):
            vals.update({'sequence_id': self.sudo()._create_sequence(vals).id})
        return super().create(vals)

    
    def unlink(self):
        seqObjs = self.mapped('sequence_id')
        seqObjs.unlink()
        return super().unlink()

    
    def write(self, vals):
        keys = ['name', 'prefix', 'padding', 'number_increment']
        seqVals = {key : vals.get(key) for key in keys if vals.get(key)}
        res = super().write(vals)
        seqVals['prefix'] = self._get_sequence_prefix(seqVals.get('prefix', ''))
        seqObjs = self.mapped('sequence_id')
        seqObjs.write(seqVals)
        return res
