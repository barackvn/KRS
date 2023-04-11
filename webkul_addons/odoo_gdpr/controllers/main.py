# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
#################################################################################

from odoo import http, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)
from odoo import http, tools, _
from werkzeug.exceptions import Forbidden
from odoo.exceptions import ValidationError

class WebsiteOdooGdpr(http.Controller):
    def _fetchDefaultData(self):
        gdpr = request.env['odoo.gdpr'].sudo().search([], limit=1)
        gdpr_data_tmpl = request.env['gdpr.data.template'].sudo().search([])
        partner = request.env.user.partner_id
        gdprRequest = request.env['gdpr.request'].sudo().search([("partner_id","=",partner.id)])
        return {
            'gdpr': gdpr,
            "gdpr_data_tmpl": gdpr_data_tmpl,
            'bootstrap_formatting': True,
            'partner_id': partner.id,
            "gdprRequest": gdprRequest,
        }

    @http.route(['/my/personal_details'], type='http', auth="user", website=True)
    def payment_method(self, **kwargs):
        values = self._fetchDefaultData()
        return request.render("odoo_gdpr.config_odoo_grpd", values)

    # @http.route(['/remove/personal_data'], type='http', auth='public', methods=["POST"], csrf=True ,website=True)
    # def RemovePersonalData(self,**kwargs):
    #     values = self._fetchDefaultData()
    #     _logger.info("--------inside RemovePersonalData--%r---",kwargs)
    #     requestObj = request.env['gdpr.request'].sudo()
    #     if not self._checkAlreadyRequest(requestObj,kwargs):
    #         requestVals = {
    #             "partner_id": kwargs.get("partner_id"),
    #             "operation_type": kwargs.get("operation_type"),
    #             "object_id": kwargs.get("object_id") or False,
    #             "action_type": kwargs.get("action_type"),
    #             "state": self._getstate("delete")
    #         }
    #         requestObj.create(requestVals)
    #         values.update({"show_alert":True})
    #     return request.render("odoo_gdpr.config_odoo_grpd", values)

    def _getstate(self,action_type):
        gdprObj = request.env['odoo.gdpr'].sudo().search([], limit=1)
        state = "pending"
        if action_type == "download":
            state = gdprObj.download_request
        elif action_type == "delete":
            state = gdprObj.delete_request
        return state


    def _checkAlreadyRequest(self,requestObj,data):
        domain= [
                    ("partner_id","=",int(data.get("partner_id"))),
                    ("operation_type","=",data.get("operation_type")),
                    ("object_id","=",data.get("object_id") and int(data.get("object_id"))) or False,
                    ("action_type","=",data.get("action_type")),
                    ("state", "=", "pending")
                 ]
        if req := requestObj.search(domain):
            return True
        else:
            False


    @http.route(['/download/personal_data'], type='json', auth='public', methods=["POST"], website=True)
    def DownloadData(self, **kwargs):
        values = {}
        requestObj = request.env['gdpr.request'].sudo()
        if not self._checkAlreadyRequest(requestObj,kwargs):
            requestVals = {
                "partner_id":kwargs.get("partner_id"),
                "operation_type":kwargs.get("operation_type"),
                "object_id":kwargs.get("object_id"),
                "action_type":kwargs.get("action_type"),
                "state":    self._getstate("download")
            }
            requestObj.create(requestVals)
            values |= {
                "alert": True,
                "alert_msg": _(
                    "Your 'DATA DOWNLOAD' request has been received, you can track the status of your request under 'Your Requests' tab."
                ),
            }
        else:
            values |= {
                "alert": True,
                "alert_msg": _(
                    "Have Patience, we have already received your request, you can track the status of your request under 'Your Requests' tab."
                ),
            }
        return values


    @http.route(['/delete/personal_data'], type='json', auth='public', methods=["POST"],website=True)
    def DeleteData(self, **kwargs):
        values = {}
        requestObj = request.env['gdpr.request'].sudo()
        if not self._checkAlreadyRequest(requestObj, kwargs):
            requestVals = {
                "partner_id": kwargs.get("partner_id"),
                "operation_type": kwargs.get("operation_type"),
                "object_id": kwargs.get("object_id"),
                "action_type": kwargs.get("action_type"),
                "state": self._getstate("delete")
            }
            requestObj.create(requestVals)
            values |= {
                "alert": True,
                "alert_msg": _(
                    "Your 'DATA REMOVAL' request has been received, you can track the status of your request under 'Your Requests' tab."
                ),
            }
        else:
            values |= {
                "alert": True,
                "alert_msg": _(
                    "Have Patience, we have already received your request, you can track the status of your request under 'Your Requests' tab."
                ),
            }
        return values



    @http.route(['/my/address'], type='http', auth="user", website=True)
    def my_address(self,**kwargs):
        PartnerObj = request.env['res.partner'].sudo()
        partner_id = request.env.user.partner_id
        # shippings = partner_id.child_ids
        domain = [
            ('id', 'child_of', partner_id.child_ids.ids),
            # ('id', 'not in', [partner_id.id]),
        ]

        shippings = PartnerObj.search(domain, order="id desc")

        values = {} | {"shippings":shippings,"partner_id":partner_id}
        return request.render("odoo_gdpr.my_address_template", values)

    def _get_mandatory_shipping_fields(self):
        return ["name", "street", "city", "country_id"]

    @http.route(['/my/edit/address'], type='http', methods=['GET', 'POST'], auth="public", website=True)
    def address(self, **kw):
        Partner = request.env['res.partner'].with_context(show_address=1).sudo()
        order = request.website.sale_get_order()
        mode = (False, False)

        partnerObj= request.env.user.partner_id
        partner_id = int(kw.get('partner_id', partnerObj.id))
        def_country_id = partnerObj.country_id
        values, errors = {}, {}
        if partner_id <= 0:
            return request.redirect('/shop/checkout')

        shippings = Partner.search([('id', 'child_of',partnerObj.commercial_partner_id.ids)])
        if partner_id in shippings.mapped('id'):
            mode = ('edit', 'shipping')
        else:
            return Forbidden()
        if mode:
            values = Partner.browse(partner_id)
        # IF POSTED
        if 'submitted' in kw:
            pre_values = self.values_preprocess(order, mode, kw)
            errors, error_msg = self.checkout_form_validate(mode, kw, pre_values)
            post, errors, error_msg = self.values_postprocess(order, mode, pre_values, errors, error_msg,partnerObj)

            if errors:
                errors['error_message'] = error_msg
                values = kw
            else:
                partner_id = self._checkout_form_save(mode, post, kw,partnerObj)
                if not errors:
                    return request.redirect(kw.get('callback') or '/my/address' )

        country = 'country_id' in values and values['country_id'] != '' and request.env['res.country'].browse(
            int(values['country_id']))
        country = country and country.exists() or def_country_id
        render_values = {
            'partner_id': partner_id,
            'mode': mode,
            'checkout': values,
            'country': country,
            'countries': country.get_website_sale_countries(mode=mode[1]),
            "states": country.get_website_sale_states(mode=mode[1]),
            'error': errors,
            'callback': kw.get('callback'),
        }
        return request.render("odoo_gdpr.myaddress", render_values)

    def values_preprocess(self, order, mode, values):
        return values

    def values_postprocess(self, order, mode, values, errors, error_msg,partnerObj):
        new_values = {}
        authorized_fields = request.env['ir.model']._get('res.partner')._get_form_writable_fields()
        for k, v in values.items():
            # don't drop empty value, it could be a field to reset
            if k in authorized_fields and v is not None:
                new_values[k] = v
            elif k not in ('field_required', 'partner_id', 'callback', 'submitted'):  # classic case
                _logger.debug(
                    f"website_sale postprocess: {k} value has been dropped (empty or not writable)"
                )

        new_values['customer'] = True
        new_values['team_id'] = request.website.salesteam_id and request.website.salesteam_id.id
        new_values['user_id'] = request.website.salesperson_id and request.website.salesperson_id.id

        lang = request.lang if request.lang in request.website.mapped('language_ids.code') else None
        if lang:
            new_values['lang'] = lang
        if mode[1] == 'shipping':
            new_values['parent_id'] = partnerObj.commercial_partner_id.id
            new_values['type'] = 'delivery'

        return new_values, errors, error_msg

    def checkout_form_validate(self, mode, all_form_values, data):
        error_message = []

        # Required fields from form
        required_fields = [f for f in (all_form_values.get('field_required') or '').split(',') if f]
        # Required fields from mandatory field function
        required_fields += mode[
                               1] == 'shipping' and self._get_mandatory_shipping_fields() or self._get_mandatory_billing_fields()
        # Check if state required
        country = request.env['res.country']
        if data.get('country_id'):
            country = country.browse(int(data.get('country_id')))
            if 'state_code' in country.get_address_fields() and country.state_ids:
                required_fields += ['state_id']

        error = {
            field_name: 'missing'
            for field_name in required_fields
            if not data.get(field_name)
        }
        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        Partner = request.env['res.partner']
        if data.get("vat") and hasattr(Partner, "check_vat"):
            partner_dummy = Partner.new({
                'vat': data['vat'],
                'country_id': (int(data['country_id'])
                               if data.get('country_id') else False),
            })
            try:
                partner_dummy.check_vat()
            except ValidationError:
                error["vat"] = 'error'

        if [err for err in error.items() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        return error, error_message

    def _checkout_form_save(self, mode, checkout, all_values,partnerObj):
        Partner = request.env['res.partner']
        if mode[0] == 'edit':
            partner_id = int(all_values.get('partner_id', 0))
            if partner_id:
                # double check
                order = request.website.sale_get_order()
                shippings = Partner.sudo().search([("id", "child_of", partnerObj.commercial_partner_id.ids)])
                if partner_id not in shippings.mapped('id') and partner_id != partnerObj.id:
                    return Forbidden()
                Partner.browse(partner_id).sudo().write(checkout)
        return partner_id
