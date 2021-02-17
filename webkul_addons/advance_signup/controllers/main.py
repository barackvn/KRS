# -*- coding: utf-8 -*-
###########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
###########################################################################

from odoo import fields, http, _
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class AuthSignupHome(AuthSignupHome):

    def do_signup(self, qcontext):
        signup_obj = request.website.get_active_website_setting()
        signup_field_list = []
        if signup_obj and signup_obj.signup_field_ids:
            required_fields = signup_obj.signup_field_ids.filtered(lambda l: l.is_required)

            # check for country state required i.e. remove state_id from required if no states in country
            required_fields_list = required_fields.mapped(lambda self: self.field.name)
            if all(item in required_fields_list for item in ['country_id','state_id']):
                if qcontext.get("country_id") and not qcontext.get("state_id"):
                    country_obj = request.env['res.country'].sudo().browse(int(qcontext.get("country_id")))
                    states = self.adv_signup_country_infos(country_obj)
                    # remove state_id from required if selected country has no states
                    if not len(states.get("states")):
                        required_fields = required_fields - required_fields.filtered(lambda l: l.field.name == "state_id")

            if required_fields:
                field_names = tuple(required_fields.mapped(lambda self: self.field.name))
                values = { key: qcontext.get(key) for key in field_names }
                for k,v in values.items():
                    if v == '' or v == None:
                        raise UserError(_("Some required fields was not properly filled in."))
        if signup_obj and signup_obj.show_t_n_c and not qcontext.get('adv_signup_t_n_c'):
            raise UserError(_("Please agree to the Terms and Conditions"))
        return super(AuthSignupHome, self).do_signup(qcontext)

    def _signup_with_values(self, token, values):
        signup_obj = request.website.get_active_website_setting()
        params = dict(request.params)
        fields_list = signup_obj.signup_field_ids.mapped(lambda self: self.field.name)
        if signup_obj and signup_obj.show_t_n_c and params.get('adv_signup_t_n_c'):
            del params['adv_signup_t_n_c']
        if params:
            if params.get('country_id'):
                params.update({'country_id':int(params.get('country_id')) })
            if params.get('state_id'):
                params.update({'state_id':int(params.get('state_id')) })
            values.update(dict((k, params[k]) for k in fields_list if k in params))
        return super(AuthSignupHome, self)._signup_with_values(token, values)

    @http.route(['/adv_signup/country_infos/<model("res.country"):country>'], type='json', auth="public", methods=['POST'], website=True)
    def adv_signup_country_infos(self, country, **kw):
        states = country.sudo().state_ids
        return dict(
            states=[(st.id, st.name) for st in states],
        )
