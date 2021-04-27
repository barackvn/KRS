from odoo import http
from odoo.http import request
import requests
import base64
import json
import xmlrpc.client as xmlrpc
from datetime import datetime, timedelta
import json
import logging

import requests
from odoo import http

_logger = logging.getLogger(__name__)



class Custom_google_calendar_controller(http.Controller):
    @http.route('/get_auth_code', type="http", auth="public", website=True)
    def get_auth_code(self, **kwarg):
        client_details = http.request.env['res.users'].sudo().search([], limit=1).company_id
        login_user_id = http.request.env['res.users'].sudo().search([('id', '=', http.request.uid)], limit=1)
        # print("\n\n\nlogin_user_id\t\t",login_user_id,"\t\tclient_details",client_details)
        
        if kwarg.get('code'):
            '''Get access Token and store in object'''
            # print("\n\n\n=================kwarg.get('code')", kwarg.get('code'), "\n\n\n")
          
            login_user_id.write({'authorization_code': kwarg.get('code')})
            if client_details:
                client_id = client_details.client_id
                client_secret = client_details.client_secret
                redirect_uri = client_details.redirect_uri
                request_token_url = 'https://accounts.google.com/o/oauth2/token'
                headers = {"Content-type": "application/x-www-form-urlencoded"}
                data = {
                    'code': kwarg.get('code'),
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'redirect_uri': redirect_uri,
                    'grant_type': "authorization_code"
                }

                response = requests.request('POST', request_token_url, data=data, headers=headers)
                # print("\n\n\nresponse.status_code\t\t", response.status_code, "\n\n\n")
                # print("\n\n\nrequest===================\n\n", response.text, "\n\n")
                if response.status_code == 200:
                    parsed_token_response = json.loads(response.text.encode('utf8'))
                    # print("\n\n\nreq.get('access_token')\n\n", parsed_token_response.get('access_token'),
                    #       "\n\nparsed_token_response.get('refresh_token')\n\n",parsed_token_response.get('refresh_token'), "\n")
                    login_user_id.write({"access_token": parsed_token_response.get('access_token'),
                                    "refresh_token": parsed_token_response.get('refresh_token')})

                    url = "https://www.googleapis.com/calendar/v3/calendars/primary"
                    bearer = 'Bearer' + parsed_token_response.get('access_token')
                    headers = {
                        'Content-Type': "application/json",
                        'Authorization': bearer
                    }

                    requests_response = requests.request("GET", url, headers=headers)
                    if requests_response.status_code == 200:
                        parsed_response = requests_response.json()
                        login_user_id.write({'calendar_id': parsed_response.get('id')})
                return "You can Close this window now"
