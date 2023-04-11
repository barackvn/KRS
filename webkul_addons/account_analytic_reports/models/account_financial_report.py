# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   @License       : https://store.webkul.com/license.html
###############################################################################
import time
from odoo import api, fields, models, _

class AccountingReport(models.TransientModel):
    _inherit = "accounting.report"

    analytic_account_ids = fields.Many2many('account.analytic.account', string='Analytic Accounts')

    def _print_report(self, data):
        if self.analytic_account_ids:
            analytic_account = [lt.name for lt in self.analytic_account_ids]
            data['form'].update({'analytic_account':analytic_account})
        data['form'].update(self.read(['analytic_account_ids'])[0])
        return super(AccountingReport,self)._print_report(data)


    def _build_contexts(self, data):
        result = super(AccountingReport, self)._build_contexts(data)
        result['analytic_account_id'] = 'analytic_account_ids' in data['form'] and data['form']['analytic_account_ids'] or False
        return result

    def check_report(self):
        res = super(AccountingReport, self).check_report()
        data = {
            'form': self.read(
                [
                    'date_from',
                    'date_to',
                    'journal_ids',
                    'target_move',
                    'analytic_account_ids',
                    'company_id',
                ]
            )[0]
        }
        used_context = self._build_contexts(data)
        res['data']['form']['used_context'] = dict(used_context, lang=self.env.context.get('lang') or 'en_US')
        return res

class ReportFinancial(models.AbstractModel):
    _inherit = 'report.accounting_pdf_reports.report_financial'

    @api.model
    def get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        if data.get('form').get('used_context')['analytic_account_id']:
            data.get('form').get('used_context')['analytic_account_ids'] = self.env['account.analytic.account'].browse(data.get('form').get('used_context')['analytic_account_id'])
        report_lines = self.get_account_lines(data.get('form'))
        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_account_lines': report_lines,
        }
