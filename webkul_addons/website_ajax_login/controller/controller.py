# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
#################################################################################
from odoo.http import route,request
import logging
from odoo import http,SUPERUSER_ID
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.tools.translate import _
import odoo
import re
import werkzeug
import json
from odoo.addons.auth_oauth.controllers.main import OAuthLogin
from odoo.addons.auth_signup.models.res_users import SignupError

_logger = logging.getLogger(__name__)

class wk_ajax_signin(http.Controller):
    """ custom login and sign up methods on controllers"""
    """ called from js using  json Rpc"""

    @http.route('/web/session/wk_check', type='json', auth="none")
    def get_session_info(self):
        values = {}
        if request.env.user:
            values["wk_login"] = True
        else:
            values["wk_login"] = False
        web_config_obj = request.env["res.config.settings"].sudo().get_values()
        values["show_ajax_form_always"] = web_config_obj.get("show_ajax_form_always")
        values["wk_block_ui"] = web_config_obj.get("wk_block_ui")
        return values

    @http.route('/shop/login/', type='json', auth='public', website=True)
    def wk_login(self, *args, **kwargs):
        values = request.params.copy()
        values.update({'message':'','status':True})
        if not request.session.db:
            values['message'] = "No Database Selected"
            values['status'] = False
        if not request.uid:
            request.uid = SUPERUSER_ID

        if ((not kwargs.get('redirect')) or (kwargs.get('redirect') and not kwargs['redirect'])):
            kwargs['redirect'] = "/web"
        values['redirect'] = kwargs['redirect']
        old_uid = request.uid
        try:
            uid = request.session.authenticate(request.session.db, values['login'], values['password'])
            values['uid'] = uid
            if uid is not False:
                values['message'] = "sucessfully login"
                return values
        except odoo.exceptions.AccessDenied as e:
            values['uid'] = False
            values['message'] = "Wrong login/password"
            return values


    @http.route('/website_ajax_login/signup', type='json', auth="public", website=True)
    def wk_signup(self, *args, **kw):
        res = {}
        qcontext = request.params.copy()
        try :
            res = self.custom_validate(qcontext)
            values = dict((key, qcontext.get(key)) for key in ('login', 'name', 'password'))
            if res['error'] == "":
                token = ""
                db, login, password = request.env['res.users'].sudo().signup(values, token)
                request.env.cr.commit()     # as authenticate will use its own cursor we need to commit the current transaction
                uid = request.session.authenticate(db, login, password)
                com = request.cr.commit()
                res['com'] = com
                res['uid'] = uid
                res["redirect"] = qcontext["redirect"] if qcontext.get("redirect", False) else "/"
        except Exception as  e:
            res['error'] = _(e.message)
        return res

    def custom_validate(self,qcontext):
        values = dict((key, qcontext.get(key)) for key in ('login', 'name', 'password',))
        pattern = '^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$'

        res={}
        res['error']=""
        if not all([k for k in values.values()]):
            res['error'] = res.setdefault('error', '') + ",filled"
            return res
        if not re.match(pattern, values.get('login')):
            res['error'] = res.setdefault('error', '') + ",email"
            return res

        users = request.env['res.users'].sudo().search([('login','=',values.get('login'))])
        if len(users):
             res['error'] = res.setdefault('error', '')+",register"
             return res
        if values.get('password') != qcontext.get('confirm_password'):
            res['error'] = res.setdefault('error', '')+",confirm_password"
            return res
        return res

class AuthSignupHome(AuthSignupHome):


    @http.route('/website_ajax_login/reset_password', type='json', auth='public', website=True)
    def wk_reset_password(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('reset_password_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext:
            try:
                login = qcontext.get('login')
                assert login, _("No login provided.")
                _logger.info(
                    "Password reset attempt for <%s> by user <%s> from %s",
                    login, request.env.user.login, request.httprequest.remote_addr)
                request.env['res.users'].sudo().reset_password(login)
                qcontext['message'] = _("An email has been sent with credentials to reset your password")
            except SignupError:
                qcontext['error'] = _("Could not reset your password")
                _logger.exception('error when resetting password')
            except Exception as e:
                qcontext['error'] = str(e)
        return qcontext



class OAuthLogin(OAuthLogin):
    def list_providers(self):
        root_url = request.httprequest.url_root
        root_url = root_url if root_url[:5] == "https" else "https" + root_url[4:]
        try:
            providers = request.env['auth.oauth.provider'].sudo().search_read([('enabled', '=', True)])
        except Exception:
            providers = []
        for provider in providers:
            return_url = root_url + 'auth_oauth/signin'
            state = self.get_state(provider)
            params = dict(
                response_type='token',
                client_id=provider['client_id'],
                redirect_uri=return_url,
                scope=provider['scope'],
                state=json.dumps(state),
            )
            provider['auth_link'] = "%s?%s" % (provider['auth_endpoint'], werkzeug.url_encode(params))
        return providers

    """ called from js before login form show and provides provider list acivated from Genral setting"""
    """ inherited the OAuthLogin for changing the redirect parameter use in  get_state method """
    @http.route('/wk_modal_login/', type='json', auth='public', website=True)
    def wk_modal_login(self,*args,**kwargs):
        url = kwargs['url']
        if werkzeug.urls.url_parse(url).path.find('/web') != 0:
            request.params['redirect'] = url
        return self.list_providers()
