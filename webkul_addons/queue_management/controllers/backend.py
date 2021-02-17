# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################

import babel
import operator

from datetime import datetime, timedelta, time

from odoo import fields, http, _
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class QMSBackend(http.Controller):

    @http.route('/queue_management/fetch_dashboard_data', type="json", auth='user')
    def fetch_dashboard_data(self, dateFrom, dateTo):
        tokenModel = request.env['token.token'].sudo()
        tokenData = self._get_today_tokens_data()
        dateDateFrom = fields.Date.from_string(dateFrom)
        dateDateTo = fields.Date.from_string(dateTo)
        dateDiffDays = (dateDateTo - dateDateFrom).days
        datetimeFrom = datetime.combine(dateDateFrom, time.min)
        datetimeTo = datetime.combine(dateDateTo, time.max)
        tokenDomain = [
            ('date', '>=', fields.Datetime.to_string(datetimeFrom)),
            ('date', '<=', fields.Datetime.to_string(datetimeTo))]
        tokenGrouData = tokenModel.read_group(tokenDomain, fields=['state'], groupby='state')
        sDraft = sCancel = sProg = sDone = 0
        piGraph = []
        for res in tokenGrouData:
            if res.get('state') == 'draft':
                sDraft += res['state_count']
            if res.get('state') == 'cancel':
                sCancel += res['state_count']
            if res.get('state') == 'progress':
                sProg += res['state_count']
            if res.get('state') == 'done':
                sDone += res['state_count']
        pi_data = [sDraft, sCancel, sProg, sDone]
        piGraph.append({
                'labels': ["Progress","Draft", "Cancel","Done"],
                'datasets': [
                    {
                        'fill': True,
                        'backgroundColor': [
                            '#4db8d7',
                            '#86a2c6',
                            '#b28c83',
                            '#4db8d7'],
                        'data': pi_data,
                    }
                ]
            })

        tokens = tokenModel.search(tokenDomain)
        # Graphes computation
        if dateDiffDays == 7:
            previousQmsLabel = _('Previous Week')
        elif dateDiffDays > 7 and dateDiffDays <= 31:
            previousQmsLabel = _('Previous Month')
        else:
            previousQmsLabel = _('Previous Year')

        qmsDomain = [
            ('date', '>=', dateFrom),
            ('date', '<=', dateTo)
        ]
        tokenGraph = [{
            'values': self._compute_qms_graph(dateDateFrom, dateDateTo, qmsDomain),
            'key': 'Total',
        }, {
            'values': self._compute_qms_graph(
                dateDateFrom - timedelta(days=dateDiffDays), dateDateFrom, qmsDomain, previous=True),
            'key': previousQmsLabel,
        }]

        # Department-based computation
        bestDept = []
        allDept = request.env['department.department'].search([])
        allTokens = tokenModel.search([])
        allTokensBw = tokenModel.search([
                ('date', '>=', fields.Datetime.to_string(datetimeFrom)),
                ('date', '<=', fields.Datetime.to_string(datetimeTo))])
        deptDict = {}
        deptMax = {}
        for dept in allDept:
            temp = allTokensBw.filtered(lambda obj : obj.token_dept == dept)
            deptMax[dept.name] = len(temp)
            deptDict[dept.name] = {
                'id' : dept.id,
                'cancelled' : len(temp.filtered(lambda obj : obj.state == 'cancel')),
                'served' : len(temp.filtered(lambda obj : obj.state in ['progress', 'done'])),
                }
        sortedDept = sorted(deptMax.items(), key=operator.itemgetter(1), reverse=True)
        i = 0
        for sortDpt in sortedDept:
            if i > 1 : break
            i += 1
            bestDept.append({
                'id' : deptDict[sortDpt[0]]['id'],
                'name' : sortDpt[0],
                'served' : deptDict[sortDpt[0]]['served'],
                'cancel' : deptDict[sortDpt[0]]['cancelled'],
            })

        # Ratio computation
        tokePerDay = round(float(len(allTokensBw)) / dateDiffDays, 2)
        tokenServered = tokenModel.search([
            ('state', 'in', ['progress', 'done'])
        ])

        totalCounter = request.env['queue.counter'].search([])
        crntSession = request.env['queue.process'].search([
            ('state', '=', 'opened')
        ])
        
        dashboardData = {
            'tokens': tokenData,
            'dashboards': {
                'qms' : {
                    'tokens' : len(tokens),
                    'graph' : tokenGraph,
                    'total_served' : tokenServered,
                    'pi_graph' : piGraph,
                },
                'best_dept' : bestDept,
                'at_glance' : {
                    'all_tokens' : len(allTokens),
                    'served' : len(allTokens.filtered(lambda obj : obj.state in ['progress', 'done'])),
                    'cancel' : len(allTokens.filtered(lambda obj : obj.state == 'cancel')),
                    'token_ratio' : tokePerDay,
                    'to_counter' : len(totalCounter),
                    'cu_session' : len(crntSession),
                }
            },
        }
        return dashboardData


    def _get_today_tokens_data(self):
        tokenModel = request.env['token.token'].sudo()
        timeFrom = request.env['queue.process'].start_time()
        domain = [('date', '>=', timeFrom)]
        tokens = tokenModel.search(domain)
        cancelTokens, remainTokens, serverTokens, todayQueue = [], [], [], []
        if tokens:
            cancelTokens = tokens.filtered(lambda obj : obj.state == 'cancel').ids
            remainTokens = tokens.filtered(lambda obj : obj.state == 'draft').ids
            serverTokens = tokens.filtered(lambda obj : obj.state not in ['cancel', 'draft']).ids
            todayQueue = list(set(tokens.ids) - set(cancelTokens))

        vals = {
            'cancel' : [cancelTokens, len(cancelTokens)],
            'served' : [serverTokens, len(serverTokens)],
            'inqueue' : [todayQueue, len(todayQueue)],
            'left' : [remainTokens, len(remainTokens)],
        }
        return vals


    def _compute_qms_graph(self, dateFrom, dateTo, qmsDomain, previous=False):

        daysBetween = (dateTo - dateFrom).days
        dateList = [(dateFrom + timedelta(days=x)) for x in range(0, daysBetween + 1)]

        dailyTokens = request.env['token.token'].sudo().read_group(
            domain=qmsDomain,
            fields=['date'],
            groupby='date:day')

        dailyTokensDict = {p['date:day']: p['date_count'] for p in dailyTokens}

        tokensGraph = [{
            '0': fields.Date.to_string(d) if not previous else fields.Date.to_string(d + timedelta(days=daysBetween)),
            # Respect read_group format in models.py
            '1': dailyTokensDict.get(babel.dates.format_date(d, format='dd MMM yyyy', locale=request.env.context.get('lang') or 'en_US'), 0)
        } for d in dateList]

        return tokensGraph