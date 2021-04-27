# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
import requests
import base64
from dateutil.parser import parse as duparse
from odoo import api, fields, models
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class CustomResUsers(models.Model):
    _inherit = "res.users"

    refresh_token = fields.Char('Refresh Token', copy=False,help="")
    access_token = fields.Char('Access Token', copy=False,help="")
    authorization_code = fields.Char("Authorization Code")
    calendar_id = fields.Char("Google CalendarId")
    
    def users_authentic(self):
        client_details = self.env['res.users'].sudo().search([('id', '=', self._context.get('uid'))],limit=1).company_id
        google_auth_endpt = 'https://accounts.google.com/o/oauth2/v2/auth?'
        access_type = 'offline'
        client_id = client_details.client_id
        redirect_uri = client_details.redirect_uri 

        url = google_auth_endpt + 'scope=https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.events&access_type='+ access_type +'&include_granted_scopes=true&response_type=code&redirect_uri=' + redirect_uri + '&client_id=' + client_id
        # print("@@@@@@@@@@@@URL@@@@@@@@@@@@",url)
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new"
        }

    def generate_refresh_token_from_access_token(self):
        client_crendtials_obj = self.env['res.users'].sudo().search([('id', '=', self._context.get('uid'))],limit=1).company_id
        # print("\n\n\nclient_crendtials_obj\t\t",client_crendtials_obj,"\n\n")
        client_id = client_crendtials_obj.client_id
        # print("\n\n\nclient_id\t\t",client_id,"\n\n")
        client_secret = client_crendtials_obj.client_secret
        redirect_uri = client_crendtials_obj.redirect_uri
        google_token_endpt = 'https://accounts.google.com/o/oauth2/token'
        auth_code = self.authorization_code
        refresh_token = self.refresh_token

        combine = client_id + ':' + client_secret
        userAndPass = base64.b64encode(combine.encode()).decode("ascii")
        # print('\n commfd ', userAndPass)

        oauth2_token = self.access_token

        headers = {'Authorization': 'Bearer {}'.format(oauth2_token)}
        payload = {
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
        }

        refresh_token_response = requests.request("POST", google_token_endpt, headers=headers, data=payload)
        # print("\n\n\nrefresh_token_response.status_code\t\t",refresh_token_response.status_code,"\n\n\n")
        # print("\n\n",refresh_token_response.text,"\n\n")
        if refresh_token_response.status_code == 200:
            parsed_response = refresh_token_response.json()
            self.access_token = parsed_response.get('access_token')
        elif refresh_token_response.status_code == 401:
            _logger.error("Access token/refresh token is expired")
        else:
            raise Warning("We got a issue !!!! Desc : {}".format(refresh_token_response.text))


            