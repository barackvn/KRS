# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################

from datetime import datetime
import json
import logging
import werkzeug.utils
import base64

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Binary
_logger = logging.getLogger(__name__)


class Binary(Binary):

    @http.route(['/web/content',
        '/web/content/<string:xmlid>',
        '/web/content/<string:xmlid>/<string:filename>',
        '/web/content/<int:id>',
        '/web/content/<int:id>/<string:filename>',
        '/web/content/<int:id>-<string:unique>',
        '/web/content/<int:id>-<string:unique>/<string:filename>',
        '/web/content/<int:id>-<string:unique>/<path:extra>/<string:filename>',
        '/web/content/<string:model>/<int:id>/<string:field>',
        '/web/content/<string:model>/<int:id>/<string:field>/<string:filename>'], type='http', auth="public")
    def content_common(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                       filename=None, filename_field='datas_fname', unique=None, mimetype=None,
                       download=None, data=None, token=None, access_token=None, related_id=None, access_mode=None,
                       **kw):
        # if 'token_' in filename:
            # download = True
        res = super(Binary, self).content_common(xmlid=xmlid, model=model, id=id, field=field,
                    filename=filename, filename_field=filename_field, unique=unique,
                    mimetype=mimetype, download=download, data=data, token=token, 
                    access_token=access_token, related_id=related_id, access_mode=False, **kw)
        return res


class QmsController(http.Controller):

    @http.route(['/qms/web/processing/<int:session>'], type='http', auth='user')
    def qms_processing(self, debug=False, session=False, **k):
        context = self.get_processing_session(session)
        if session:
            return request.render('queue_management.queue_index', qcontext=context)

    def get_processing_session(self, sessionId):
        qProcessModel = request.env['queue.process'].sudo()
        if not sessionId:
            qProcess = qProcessModel.search([
                ('state', '=', 'opened'),
                ('user_id', '=', request.session.uid)], limit=1)
        else:
            qProcess = qProcessModel.browse(sessionId)
        if not qProcess:
            return werkzeug.utils.redirect('/web#action=queue_management.action_client_qms_menu')
        department = qProcess.dept_id
        company = request.env.user.company_id
        tokens = self._get_today_tokens()
        today = datetime.today()
        tdDate = today.strftime('%d %b %Y')
        context = {
            'session_info': json.dumps(request.env['ir.http'].session_info()),
            'qp_session': qProcess.id,
            'user': qProcess.user_id,
            'department': department,
            'counter': qProcess.config_id,
            'mode': 'processing_queue',
            'tdate': tdDate,
            'tokens': tokens,
            'company': company,
        }
        return context

    @http.route('/qms/web/session/<int:session>', type='http', auth='user')
    def qms_web(self, debug=False, session=False, **k):
        context =  self.get_token_session(session)
        return request.render('queue_management.index', qcontext=context)

    def get_token_session(self, sessionId):
        tokenSessionModel = request.env['token.session'].sudo()
        if not sessionId:
            tokenSession = tokenSessionModel.search([
                ('state', '=', 'opened'),
                ('user_id', '=', request.session.uid)], limit=1)
        else:
            tokenSession = tokenSessionModel.browse(sessionId)
        if not tokenSession:
            return werkzeug.utils.redirect('/web#action=queue_management.action_client_qms_menu')
        departments = request.env['department.department'].sudo().search([])
        company = request.env.user.company_id

        context = {
            'session_info': json.dumps(request.env['ir.http'].session_info()),
            't_session': tokenSession.id,
            'departments': departments,
            'mode': 'details',
            'company': company,
        }
        return context

    @http.route('/queue/status', type='http', auth='user')
    def qms_token_status(self, debug=False, session=False, **k):
        context =  self.get_today_status()
        return request.render('queue_management.queue_status', qcontext=context)

    def get_today_status(self):
        allDepts = request.env['department.department'].sudo().search([])
        company = request.env.user.company_id
        qProcess = request.env['queue.process'].sudo()
        timeFrom = qProcess.start_time()
        dateFrom = datetime.strptime(timeFrom, "%Y-%m-%d %H:%M:%S")
        screenList = []
        for dept in allDepts:
            counters = []
            openQs = qProcess.search([
                ('dept_id', '=', dept.id),
                ('state', 'in', ['opened', 'closing_control'])
            ])
            for openQ in openQs:
                qConter = openQ.config_id
                tokenDate = qConter.current_token_day
                crntToken = '000'
                if tokenDate:
                    # tokenTime = datetime.strptime(tokenDate, "%Y-%m-%d %H:%M:%S")
                    if tokenDate >= dateFrom:
                        crntToken = qConter.current_token
                counters.append({
                    'counter' : qConter.name or '-',
                    'token' : crntToken
                })
            if counters:
                screenList.append({
                    'department' : dept.name,
                    'id' : dept.id,
                    'counters' : counters,
                })
                break
        
        return {'to_display' : screenList, 'company' : company}


    def get_queue_status_data(self, offset):
        qProcess = request.env['queue.process'].sudo()
        depts = request.env['department.department'].sudo().search(
            [], limit=1, offset=offset, order="id asc")
        deptDiv = '''<div class="dept_div">{}{}</div>'''
        deptLable =  '''<div style="text-align:center;">
                            <label class="dept_label">{}</label>
                    </div>'''
        deptCounterlist = []
        deptCounter = '''<div class="dep_counter">
                            <div class="dep_counter_token">
                                    <span  class="counter_tokenno">
                                        {}
                                    </span>
                            </div>
                            <div class="dep_counter_name">
                                {}
                            </div>
                        </div>'''
        moreRec = False
        timeFrom = qProcess.start_time()
        dateFrom = datetime.strptime(timeFrom, "%Y-%m-%d %H:%M:%S")
        for dept in depts:
            deptLable = deptLable.format(dept.name)
            openQs = qProcess.search([
                ('dept_id', '=', dept.id),
                ('state', 'in', ['opened', 'closing_control'])
            ])
            for openQ in openQs:
                moreRec = True
                qConter = openQ.config_id
                tokenDate = qConter.current_token_day
                crntToken = '000'
                if tokenDate:
                    # tokenTime = datetime.strptime(tokenDate, "%Y-%m-%d %H:%M:%S")
                    if tokenDate >= dateFrom:
                        crntToken = qConter.current_token
                deptCounterlist.append(deptCounter.format(crntToken, qConter.name))
        deptDiv = deptDiv.format(deptLable, ''.join(deptCounterlist))
        dataDict =  {
            'deptDiv': deptDiv,
            'more' : moreRec,
            'depts' : depts,
            'offset' : offset,
            'reset' : False
        }
        return dataDict

    @http.route(['/counter/status/'], type='json', auth="user", methods=['POST'])
    def counter_status(self, offset):
        dataDict = self.get_queue_status_data(offset)
        moreRec = dataDict.get('more')
        detpLeft = dataDict.pop('depts', False)
        while not moreRec:
            if detpLeft:
                offset += 1
                dataDict = self.get_queue_status_data(offset)
                moreRec = dataDict.get('more')
                detpLeft = dataDict.pop('depts', False)
            else:
                dataDict.update({'reset' : True})
                break
        return dataDict

    @http.route(['/today/tokens/'], type='json', auth="user", methods=['POST'])
    def page_tokens(self, offset, session):
        tokenModel = request.env['token.token']
        timeFrom = request.env['queue.process'].start_time()
        domain = [('state', '!=', 'cancel'), ('date', '>=', timeFrom)]
        tokens = tokenModel.search(domain, limit=7, offset=offset, order="id asc")
        rList = []
        tbody = "<tbody id='token_body'>{}</tbody>"
        tr = "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>"
        moreRec = False
        for token in tokens:
            moreRec = True
            tNo = token.token_day_number
            tCounter = token.queue_session and token.queue_session.config_id.name or '-'
            tCall = token.process_by.name or '-'
            tRecall = '-'
            if token.process_by:
                tRecall = '''
                    <a href="/token/recall/?session={}&amp;token={}">
                        <img src="/queue_management/static/src/img/recall.png" height="18px;"/>
                    </a>
                '''
                tRecall = tRecall.format(session, token.id)
            rList.append(tr.format(tNo, tCounter, tNo, tCall, tRecall))
        tbody = tbody.format(''.join(rList))
        return {'tbody': tbody, 'more' : moreRec}
    

    def _get_today_tokens(self, offset=0):
        tokenModel = request.env['token.token'].sudo()
        timeFrom = request.env['queue.process'].sudo().start_time()
        domain = [('state', '!=', 'cancel'), ('date', '>=', timeFrom)]
        tokens = tokenModel.search(domain,limit=7, offset=offset, order="id asc")
        tokens = sorted(tokens, key=lambda tknObj: tknObj.token_day_number)
        return tokens

    @http.route(['/queue/details'], type='http', auth='user')
    def generate_token(self, **k):
        company = request.env.user.company_id
        tokenModel = request.env['token.token'].sudo()
        token_session = request.env['token.session'].sudo()
        irAttach = request.env['ir.attachment'].sudo()
        tokenSessionId = int(k.get('t_session_id'))
        vals = {
            'token_session': tokenSessionId,
            'token_dept': int(k.get('dept_id')),
            'user_mobile': k.get('phone'),
            'name': k.get('name'),
        }
        tokenObj = tokenModel.create(vals)
        pdf = request.env.ref('queue_management.action_report_token').sudo(
        ).render_qweb_pdf([tokenObj.id])[0]
        base64Data = base64.b64encode(pdf)
        fName = 'token_' + str(tokenObj.id) + '.pdf'
        vals = {
            'datas': base64Data,
            'type' : 'binary',
            'res_model': 'token.token',
            'res_id': tokenObj.id,
            'db_datas': fName,
            # 'datas_fname': fName,
            'name': fName,
            'public' : True,
        }
        attachmentId = irAttach.create(vals)
        tokenObj.attachment_id = attachmentId.id
        isPrinter = self.check_printer()
        session_obj = token_session.browse(tokenSessionId)
        token_interface = session_obj.config_id
        ip_addr = False
        if token_interface.use_posbox and token_interface.proxy_ip_addr:
            ip_addr = token_interface.proxy_ip_addr
        currentToken = self._get_current_token()
        if currentToken == '0':
            myPosition = tokenObj.token_day_number
        else:
            myPosition = str(int(tokenObj.token_day_number) - int(currentToken))
        context = {
            'mode': 'print',
            'tokenObj': tokenObj,
            'token_attending': currentToken,
            'currnet_po': myPosition,
            'company': company,
            'attachment_id': attachmentId.id,
            't_session': tokenSessionId,
            'is_printer': isPrinter,
            'ip_addr' : ip_addr,
        }
        return request.render('queue_management.index', qcontext=context)

    def _get_current_token(self):
        tokenModel = request.env['token.token'].sudo()
        timeFrom = request.env['queue.process'].sudo().start_time()
        domain = [('state', 'not in', ['draft', 'cancel']), ('date', '>=', timeFrom)]
        tokenNo = tokenModel.search(domain).mapped('token_day_number')
        if tokenNo:
            tokenNo = sorted(tokenNo)
            currentToken = tokenNo[-1].zfill(3)
        else:
            currentToken = '0'
        return currentToken
        
    @http.route(['/token/cancel'], type='http', auth='user')
    def cancel_token(self, **k):
        tokenObj = request.env['token.token'].sudo().browse(int(k.get('token')))
        tokenObj.write({
            'state': 'cancel',
            'cust_query': 'Cancelled by user({}) himself'.format(tokenObj.name)
            })
        context = self.get_token_session(int(k.get('session')))
        return request.render('queue_management.index', qcontext=context)

    @http.route(['/token/print'], type='http', auth='user')
    def print_token(self, **k):
        context = self.get_token_session(int(k.get('session')))
        return request.render('queue_management.index', qcontext=context)


    @http.route(['/session/close/<int:session>'], type='http', auth="user")
    def close_session(self, session):
        sessionObj = request.env['token.session'].sudo().browse(session)
        sessionObj.action_session_closing_control()
        return werkzeug.utils.redirect('/web#action=queue_management.action_client_qms_menu')

    @http.route(['/qms/process/next'], type='http', auth='user')
    def process_next_token(self, **k):
        tokenModel = request.env['token.token'].sudo()
        qProcessModel = request.env['queue.process'].sudo()
        qEmpty = False
        mode = 'token_details'
        msg = ''
        qProcess = qProcessModel.browse(int(k.get('session')))
        dept = qProcess.dept_id.id
        timeFrom = qProcessModel.start_time()
        domain = [('state', 'not in', ['cancel']),
                  ('date', '>=', timeFrom),
                  ('token_dept', '=', dept),
                  ]
        deptTokens = tokenModel.search(domain, order='id asc')
        inDraft = deptTokens.filtered(lambda obj: obj.state == 'draft')
        nextToken = inDraft and inDraft[0] or inDraft
        if not inDraft:
            msg = 'Note : Queue is empty for {} department'.format(qProcess.dept_id.name)
            qEmpty = True
            mode = 'processing_queue'
        else:
            nextToken = inDraft and inDraft[0]
            nextToken.write({
                'state': 'progress',
                'process_by': request.session.uid,
                'queue_session': int(k.get('session')),
            })
            qProcess.config_id.current_token = nextToken and nextToken.token_day_number or '000'
            qProcess.config_id.current_token_day = nextToken and nextToken.date or ''

        context = self.get_processing_session(int(k.get('session')))
        context.update({
            'next_token': nextToken,
            'empty_queue': qEmpty,
            'msg' : msg,
            'mode': mode,
            'states': [('done', 'Done'),
                    ('progress', 'Progress'),
                    ('cancel', 'Cancel')]
        })
        if int(k.get('session')):
            return request.render('queue_management.queue_index', qcontext=context)

    @http.route(['/process/next/token'], type='http', auth='user')
    def next_token_submit(self, **k):
        tokenModel = request.env['token.token'].sudo()
        qProcessId = int(k.get('qp_session_id'))
        tokenObj = tokenModel.browse(int(k.get('token')))
        state = k.get('token_state')
        tokenObj.write({
            'state': state,
            'cust_query': k.get('cust_query'),
            'feedback': k.get('admin_feedback'),
            'process_by': request.session.uid,
            'queue_session': qProcessId,
        })
        context = self.get_processing_session(qProcessId)
        if qProcessId:
            return request.render('queue_management.queue_index', qcontext=context)

    @http.route(['/token/recall'], type='http', auth='user')
    def token_recall(self, **k):
        qpSessionId = int(k.get('session'))
        tokenId = int(k.get('token'))
        tokenObj = request.env['token.token'].sudo().browse(tokenId)
        context = self.get_processing_session(qpSessionId)
        context.update({
            'next_token': tokenObj,
            'mode': 'token_details',
            'states': [('done', 'Done'),
                       ('progress', 'Progress'),
                       ('cancel', 'Cancel')]
        })
        if qpSessionId:
            return request.render('queue_management.queue_index', qcontext=context)

    @http.route(['/qpsession/close/<int:session>'], type='http', auth="user")
    def close_qpsession(self, session):
        sessionObj = request.env['queue.process'].sudo().browse(session)
        sessionObj.action_session_closing_control()
        return werkzeug.utils.redirect('/web#action=queue_management.action_client_qms_menu')

    @http.route(['/status/close'], type='http', auth="user")
    def status_close(self):
        return werkzeug.utils.redirect('/web#action=queue_management.action_client_qms_menu')

    def check_printer(self, module='base_report_to_printer'):
        isBasePrinterInstl = request.env['ir.module.module'].sudo().search([
            ('name', '=', module),
            ('state', '=', 'installed')], limit=1)
        return 'yes' if isBasePrinterInstl else 'no'
