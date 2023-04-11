# -*- coding: utf-8 -*-
##########################################################################
# 2010-2017 Webkul.
#
# NOTICE OF LICENSE
#
# All right is reserved,
# Please go through this link for complete license : https://store.webkul.com/license.html
#
# DISCLAIMER
#
# Do not edit or add to this file if you wish to upgrade this module to newer
# versions in the future. If you wish to customize this module for your
# needs please refer to https://store.webkul.com/customisation-guidelines/ for more information.
#
# @Author        : Webkul Software Pvt. Ltd. (<support@webkul.com>)
# @Copyright (c) : 2010-2017 Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# @License       : https://store.webkul.com/license.html
#
##########################################################################
from odoo.http import route,request
import logging
from odoo import http
from odoo.tools.translate import _
from odoo.addons.website_ajax_login.controller.controller import wk_ajax_signin
import re
import json
import werkzeug
from ast import literal_eval

_logger = logging.getLogger(__name__)

class wk_ajax_signin(wk_ajax_signin):
    """ custom login and sign up methods on controllers"""
    """ called from js using  json Rpc"""

    def custom_validate(self,qcontext):
        if qcontext.get('is_seller'):
            values = {
                key: qcontext.get(key)
                for key in (
                    'login',
                    'name',
                    'password',
                    'is_seller',
                    'country_id',
                    'url_handler',
                    'mp_terms_conditions',
                )
            }
        else:
            values = {key: qcontext.get(key) for key in ('login', 'name', 'password',)}
        pattern = '^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$'
        res = {'error': ""}
        if not all(list(values.values())):
            res['error'] = res.setdefault('error', '') + ",filled"
            return res
        if not re.match(pattern, values.get('login')):
            res['error'] = res.setdefault('error', '') + ",email"
            return res

        users=request.env['res.users'].sudo().search([('login','=',values.get('login'))])
        if  len(users):
            res['error'] = res.setdefault('error', '')+",register"
            return res
        if  values.get('password') != qcontext.get('confirm_password'):
            res['error'] = res.setdefault('error', '')+",confirm_password"
            return res

        if values.get('url_handler'):
            if not re.match('^[a-zA-Z0-9-_]+$', values.get('url_handler')) or re.match('^[-_][a-zA-Z0-9-_]*$', values.get('url_handler')) or re.match('^[a-zA-Z0-9-_]*[-_]$', values.get('url_handler')):
                res['error'] = res.setdefault('error', '')+",url_incorrect"
            sameurl = request.env["res.partner"].sudo().search([('url_handler', '=', values.get('url_handler'))])
            if sameurl:
                res['error'] = res.setdefault('error', '')+",url_not_available"

        return res

    def get_redirect_url(self, uid):
        if uid:
            user_obj = request.env["res.users"].browse(uid)
            group_portal = request.env['ir.model.data'].sudo().get_object_reference('base', 'group_portal')[1]
            read_data_list = user_obj.sudo().read()
            for data in read_data_list:
                groups_id = data['groups_id'] if read_data_list else []
            if user_obj and user_obj.partner_id.seller:
                return "/my/marketplace"
            elif user_obj and group_portal in groups_id:
                return "/shop"
            else:
                return "/web"
        return False


    @http.route('/shop/login/', type='json', auth='public', website=True)
    def wk_login(self,*args,**kwargs):
        res = super(wk_ajax_signin, self).wk_login(*args, **kwargs)
        if uid := res.get("uid", False):
            if wk_url := self.get_redirect_url(res.get("uid")):
                res.update({"redirect":wk_url})
        return res


    @http.route('/website_ajax_login/signup', type='json',auth="public",website=True)
    def wk_signup(self, *args,**kw):
        res={}
        qcontext =  request.params.copy()
        country_id = qcontext.get('country_id')
        try:
            res=self.custom_validate(qcontext)
            values = {key: qcontext.get(key) for key in ('login', 'name', 'password')}
            if qcontext.get('is_seller'):
                values |= {
                    'is_seller': True,
                    'country_id': int(country_id) if country_id else country_id,
                    'url_handler': qcontext.get('url_handler'),
                }
            if res['error']=="":
                token=""
                db, login, password = request.env['res.users'].sudo().signup(values, token)
                request.env.cr.commit()     # as authenticate will use its own cursor we need to commit the current transaction
                uid = request.session.authenticate(db, login, password)
                com=request.cr.commit()
                res['com']=com
                res['uid']=uid
                res["redirect"] = self.get_redirect_url(uid)
                # if ((not qcontext.has_key('redirect')) or (qcontext.has_key('redirect') and not qcontext['redirect'])):
                #     qcontext['redirect'] = "/shop"
                # res['redirect'] = qcontext['redirect']
                # wk_url = self.get_redirect_url(uid)
                # if wk_url :
                #     res.update({"redirect":wk_url})
        except Exception as e:
            res['error']=_(str(e))
        return res


    @http.route('/signup_as_seller_link/', type='json', auth='public', website=True)
    def signup_as_seller_link(self,is_seller,**kwargs):
        new_link = {}
        for url, link_url in kwargs.items():
            if srt := link_url.find('state'):
                end = link_url.find('&', srt)
                if end == -1:
                    end = len(link_url)
                old_state = link_url[srt:end]
                d_state = werkzeug.url_decode(old_state,cls=dict)
                state = literal_eval(d_state['state'])
                state['s'] = str(is_seller)
                d_state["state"] = json.dumps(state)
                url_link = link_url[:srt] + werkzeug.url_encode(d_state) + link_url[end:]
                new_link[url] = url_link
        return new_link
