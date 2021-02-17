# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

import logging
from odoo import http, tools, _
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_sale.controllers.main import WebsiteSale

_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):
    def checkout_values(self, **kw):
        order = request.website.sale_get_order(force_create=1)
        shippings, billings = [], []
        userId = request.session.uid
        if order.partner_id != request.website.user_id.sudo().partner_id:
            Partner = order.partner_id.with_context(show_address=1).sudo()
            shippings = Partner.search([
                ("id", "child_of", order.partner_id.commercial_partner_id.ids),
                '|', ("type", "in", ["delivery", "other"]), ("id", "=", order.partner_id.commercial_partner_id.id)
            ], order='id desc')
            billings = Partner.search([
                ("id", "child_of", order.partner_id.commercial_partner_id.ids),
                '|', ("type", "=", "invoice"), ("id", "=", order.partner_id.commercial_partner_id.id)
            ], order='id desc')
            if shippings and not kw.get('invoice_change', False):
                if kw.get('partner_id') or 'use_billing' in kw:
                    if 'use_billing' in kw:
                        partner_id = order.partner_id.id
                    else:
                        partner_id = int(kw.get('partner_id'))
                    if partner_id in shippings.mapped('id'):
                        order.partner_shipping_id = partner_id
                elif not order.partner_shipping_id:
                    last_order = request.env['sale.order'].sudo().search([("partner_id", "=", order.partner_id.id)], order='id desc', limit=1)
                    order.partner_shipping_id.id = last_order and last_order.id
            elif kw.get('invoice_change'):
                partnerId =  int(kw.get('partner_id', 0))
                if partnerId and not kw.get('callback'):
                    addrType = request.env['res.partner'].browse(partnerId).type
                    if addrType == 'invoice' and partnerId in billings.mapped('id'):
                        order.partner_invoice_id = partnerId
                elif kw.get('callback'):
                    order.partner_invoice_id = partnerId
        values = {
            'order': order,
            'shippings': shippings,
            'billings' : billings,
            'userId': userId,
            'only_services': order and order.only_services or False
        }
        return values


    def values_postprocess(self, order, addrMode, values, errors, errorMsg):
        partnerAddrId = int(values.get('partner_id', 0))
        newValues, errors, errorMsg = super(WebsiteSale, self).values_postprocess(
            order, addrMode, values, errors, errorMsg)
        userId = request.session.uid
        if addrMode[1] == 'billing' and userId:
            newValues['type'] = 'invoice'
            partnerAddrId = int(values.get('partner_id', 0))
            if partnerAddrId and partnerAddrId != order.partner_id.commercial_partner_id.id:
                newValues['parent_id'] = order.partner_id.commercial_partner_id.id
        return newValues, errors, errorMsg

    def _checkout_invoice_form_save(self, addrMode, checkout, allValues):
        Partner = request.env['res.partner']
        partnerAddrId = int(allValues.get('partner_id', 0))
        if addrMode[0] == 'new':
            partnerId = Partner.sudo().create(checkout).id
            return partnerId
        elif addrMode[0] == 'edit' and partnerAddrId:
            Partner.browse(partnerAddrId).sudo().write(checkout)
        return partnerAddrId



    @http.route(['/my/invoice/address'], type='http', methods=['GET', 'POST'], auth="public", website=True)
    def my_invoice_address(self, **kw):
        Partner = request.env['res.partner'].with_context(show_address=1).sudo()
        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        defCountryId = order.partner_id.country_id
        values, errors = {}, {}
        partnerId = int(kw.get('partner_id', -1))
        addrMode = eval(kw.get('addr_mode', "(False, False)"))
        canEditVat = False
        # IF PUBLIC ORDER
        if order.partner_id.id == request.website.user_id.sudo().partner_id.id:
            addrMode = ('new', 'billing')
            canEditVat = True
            country_code = request.session['geoip'].get('country_code')
            if country_code:
                defCountryId = request.env['res.country'].search([('code', '=', country_code)], limit=1)
            else:
                defCountryId = request.website.user_id.sudo().country_id
        # IF ORDER LINKED TO A PARTNER
        elif partnerId > 0:
            values = Partner.browse(partnerId)
        elif partnerId == -1:
            addrMode = ('new', 'billing')
        else: # no addrMode - refresh without post?
            return request.redirect('/shop/checkout')
        # IF POSTED
        if 'submitted' in kw:
            preValues = self.values_preprocess(order, addrMode, kw)
            errors, errorMsg = self.checkout_form_validate(addrMode, kw, preValues)
            post, errors, errorMsg = self.values_postprocess(order, addrMode, preValues, errors, errorMsg)

            if errors:
                errors['error_message'] = errorMsg
                values = kw
            else:
                partnerId = self._checkout_invoice_form_save(addrMode, post, kw)
                if partnerId:
                    order.partner_invoice_id = partnerId

                order.message_partner_ids = [(4, partnerId), (3, request.website.partner_id.id)]
                if not errors:
                    return request.redirect(kw.get('callback') or '/shop/checkout')

        country = 'country_id' in values and values['country_id'] != '' and request.env['res.country'].browse(int(values['country_id']))
        country = country and country.exists() or defCountryId
        renderValues = {
            'website_sale_order': order,
            'partner_id': partnerId,
            'mode': addrMode,
            'checkout': values,
            'country': country,
            'can_edit_vat': canEditVat,
            'countries': country.get_website_sale_countries(mode=addrMode[1]),
            "states": country.get_website_sale_states(mode=addrMode[1]),
            'error': errors,
            'callback': kw.get('callback'),
            'only_services': order and order.only_services,

        }
        # return request.render("website_sale.address", renderValues)
        return request.render("website_address_book.my_invocie_address", renderValues)


class CustomerPortal(CustomerPortal):

    def addr_values_preprocess(self, partnerObj, addrMode, values):
        return values

    def addr_form_validate(self, addrMode, allFormValues, data):
        # mode: tuple ('new|edit', 'billing|shipping')
        # allFormValues: all values before preprocess
        # data: values after preprocess
        error = dict()
        errorMessage = []
        # Required fields from form
        requiredFields = ["name", "street", "city", "country_id", "phone"]
        if addrMode and addrMode[1] == 'billing':
            requiredFields.append("email")
        # Check if state required
        country = request.env['res.country']
        if data.get('country_id'):
            country = country.browse(int(data.get('country_id')))
            if 'state_code' in country.get_address_fields() and country.state_ids:
                requiredFields += ['state_id']

        # error message for empty required fields
        for field_name in requiredFields:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            errorMessage.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        Partner = request.env['res.partner']
        if data.get("vat") and hasattr(Partner, "check_vat"):
            partnerDummy = Partner.new({
                'vat': data['vat'],
                'country_id': (int(data['country_id'])
                               if data.get('country_id') else False),
            })
            try:
                partnerDummy.check_vat()
            except ValidationError:
                error["vat"] = 'error'
        if [err for err in error.items() if err[1] == 'missing']:
            errorMessage.append(_('Some required fields are empty.'))

        return error, errorMessage

    def addr_values_postprocess(self, addrMode, preValues, errors, errorMsg):
        newValues = {}
        # _logger.info("addre---------------------------------**************************")

        authorized_fields = request.env['ir.model']._get('res.partner')._get_form_writable_fields()
        for k, v in preValues.items():
            # don't drop empty value, it could be a field to reset
            if k in authorized_fields and v is not None:
                newValues[k] = v
            else:  # DEBUG ONLY
                if k not in ('field_required', 'partner_id', 'callback', 'submitted'): # classic case
                    _logger.debug("website_sale postprocess: %s value has been dropped (empty or not writable)" % k)

        newValues['team_id'] = request.website.salesteam_id and request.website.salesteam_id.id
        newValues['user_id'] = request.website.salesperson_id and request.website.salesperson_id.id

        if request.website.specific_user_account:
            newValues['website_id'] = request.website.id

        if addrMode[0] == 'new':
            newValues['company_id'] = request.website.company_id.id
            if addrMode[1] == 'billing':
                newValues['type'] = 'invoice'

        lang = request.lang.code if request.lang.code in request.website.mapped('language_ids.code') else None
        if lang:
            newValues['lang'] = lang
        if addrMode == ('edit', 'billing') :
            newValues['type'] = 'invoice'
        if addrMode[1] == 'shipping':
            newValues['type'] = 'delivery'

        return newValues, errors, errorMsg

    def _addr_form_save(self, addrMode, newValues, allValues):
        Partner = request.env['res.partner']
        partnerAddrId = int(allValues.get('partner_id', 0))
        if addrMode[0] == 'new':
            newValues['parent_id'] = partnerAddrId
            partnerId = Partner.sudo().create(newValues).id
            return partnerId
        elif addrMode[0] == 'edit' and partnerAddrId:
            if newValues.get('state_id'):
                newValues.update({
                    'state_id': int(newValues.get('state_id')),
                })
            else:
                newValues.update({
                    'state_id': None,
                })

            Partner.browse(partnerAddrId).sudo().write(newValues)
        return partnerAddrId

    @http.route(['/my/addressbook'], type='http', auth="user", website=True)
    def portal_my_addressbook(self, **kw):
        partner = request.env.user.partner_id

        shippings = partner.search([
            ("id", "child_of", partner.commercial_partner_id.ids),
            '|', ("type", "=", "delivery"), ("id", "=", partner.commercial_partner_id.id)
        ], order='id desc')
        billings = partner.search([
            ("id", "child_of", partner.commercial_partner_id.ids),
            '|', ("type", "=", "invoice"), ("id", "=", partner.commercial_partner_id.id)
        ], order='id desc')
        renderValues = {
            'partner_id': partner,
            'shippings' : shippings,
            'billings' : billings,
        }
        return request.render("website_address_book.wk_my_home_address_book", renderValues)

    @http.route(['/my/address'], type='http', methods=['GET', 'POST'], auth="public", website=True)
    def my_address(self, **kw):
        partnerId = int(kw.get('partner_id', -1))
        addrMode = eval(kw.get('addr_mode', "(False, False)"))
        errors, values = {}, {}
        if partnerId < 0:
            return request.redirect('/my/addressbook')
        partnerObj = request.env['res.partner'].browse(partnerId)
        countryModel = request.env['res.country']
        defCountryId = partnerObj.country_id
        if addrMode[0] not in [False, 'new']:
            values = partnerObj
        # IF POSTED
        if 'submitted' in kw:

            preValues = self.addr_values_preprocess(partnerObj, addrMode, kw)
            errors, errorMsg = self.addr_form_validate(addrMode, kw, preValues)
            postValues, errors, errorMsg = self.addr_values_postprocess(addrMode, preValues, errors, errorMsg)
            postValues.update({
            'country_id': int(postValues['country_id']),
            })

            if errors:
                errors['error_message'] = errorMsg
                values = kw
            else:
                partnerId = self._addr_form_save(addrMode, postValues, kw)
                return request.redirect('/my/addressbook')

        country = 'country_id' in values and values['country_id'] != '' and request.env['res.country'].browse(int(values['country_id']))
        country = country and country.exists() or defCountryId
        renderValues = {
            'partner_id': partnerId,
            'partnerObj': partnerObj,
            'checkout' : values,
            'error' : errors,
            'mode': addrMode,
            'country': country,
            'countries': country.get_website_sale_countries(mode=addrMode[1]),
            "states": country.get_website_sale_states(mode=addrMode[1]),
        }
        return request.render("website_address_book.my_address", renderValues)

    @http.route(['/my/newaddress'], type='http', auth="public", website=True)
    def new_adddress(self, **post):
        return request.redirect('/my/address')

    @http.route(['/delete/address'], type='json', auth="public", methods=['POST'], website=True)
    def delete_address(self, partner_id=''):
        if partner_id:
            partner_id = int(partner_id)
            partnerObj = request.env['res.partner'].sudo().browse(partner_id)
            saleObjs = request.env['sale.order'].sudo().search(['|', ('partner_invoice_id', '=', partner_id), ('partner_shipping_id', '=', partner_id)])
            if saleObjs:
                partnerObj.active = False
            else:
                partnerObj.unlink()
        return True
