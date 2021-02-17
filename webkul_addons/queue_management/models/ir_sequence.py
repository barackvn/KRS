# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################

from datetime import datetime, timedelta
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    def _next(self, sequence_date=None):
        ctx = dict(self._context or {})
        if self._context.get('token_day'):
            seqDateRangeModel = self.env['ir.sequence.date_range']
            tokenDate = self._context.get('token_day')
            dateTo = tokenDate + timedelta(days=1)
            domain = [
                ('sequence_id', '=', self.id),
                ('date_from', '=', tokenDate),
                ('date_to', '=', dateTo)
            ]
            seqDate = seqDateRangeModel.sudo().search(domain, limit=1)
            if not seqDate:
                seqDate = seqDateRangeModel.sudo().create({
                    'date_from': tokenDate,
                    'date_to': dateTo,
                    'sequence_id': self.id,
                })
            return seqDate.with_context(ir_sequence_date_range=seqDate.date_from)._next()
        return super(IrSequence, self)._next(sequence_date=sequence_date)


    # def _next(self, sequence_date=None):
    #     """ Returns the next number in the preferred sequence in all the ones given in self."""
    #     if not self.use_date_range:
    #         return self._next_do()
    #     # date mode
    #     dt = sequence_date or self._context.get('ir_sequence_date', fields.Date.today())
    #     seq_date = self.env['ir.sequence.date_range'].search([('sequence_id', '=', self.id), ('date_from', '<=', dt), ('date_to', '>=', dt)], limit=1)
    #     if not seq_date:
    #         seq_date = self._create_date_range_seq(dt)
    #     return seq_date.with_context(ir_sequence_date_range=seq_date.date_from)._next()