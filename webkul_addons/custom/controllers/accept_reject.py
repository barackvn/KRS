from odoo import fields,api, http, tools, _
from odoo.http import request

import babel.dates
import re
import werkzeug
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.addons.website.controllers.main import QueryURL

# from odoo.addons.website.models.website import slug
from odoo.addons.http_routing.models.ir_http import slug

import logging

class ApproveSample(http.Controller):

    @http.route('/approve/<string:id>', type='http', auth="user", methods=['GET', 'POST'], website=True,
                csrf=False)
    def approval_details(self, id, **post):
        msg_vals_manager_seller = {}
        msg_vals_manager_admin = {}

        sample_data = request.env['crm.lead'].sudo().search([('id', '=', int(id))], limit=1)
        sample_data = request.env['crm.lead'].sudo().search([('id', '=', int(id))], limit=1)
        stage = request.env['crm.stage'].sudo().search([('name', '=', 'Accepted')], limit=1)
        for crm in sample_data:
            crm.sudo().write({'stage_id': stage.id})

            msg_vals_manager_seller.update({
                'body_html': """ Thanks for approving the membership.<br/> Here are your details:<br/> 
                                        Text: Sending samples to Kairos for 360° view pictures<br/>
                                        Attachment: Excel file about the calculation of the fulfilment<br/>
                                        Link: <a href="http://localhost:8074/web#id=&action=969&model=survey.landing&view_type=form&cids=&menu_id=295">Enter shop details here.</a> <br/>"""
            })

            msg_vals_manager_seller.update({
                'subject': 'Membership Approval',
                'email_to': crm.email_from,
            })
            msg_id_manager_seller = request.env['mail.mail'].create(msg_vals_manager_seller)
            msg_id_manager_seller.send()

            msg_vals_manager_admin.update({
                'body_html': """ Seller has approved the membership."""
            })

            msg_vals_manager_admin.update({
                'subject': 'Membership Approval',
                'email_to': 'admin@sophiesgarden.be',
            })
            msg_id_manager_admin = request.env['mail.mail'].create(msg_vals_manager_admin)
            msg_id_manager_admin.send()

            return request.redirect('/my/home')

    @http.route('/reject/<string:id>', type='http', auth="user", methods=['GET', 'POST'], website=True,
                csrf=False)
    def reject_details(self, id, **post):
        msg_vals_manager_seller = {}
        msg_vals_manager_admin = {}



        sample_data = request.env['crm.lead'].sudo().search([('id', '=', int(id))], limit=1)
        stage = request.env['crm.stage'].sudo().search([('name', '=', 'Rejected')], limit=1)
        for sale in sample_data:
            sale.sudo().write({'stage_id': stage.id})

            msg_vals_manager_seller.update({
                'body_html': """ Sorry we could not meet your expectations."""
            })

            msg_vals_manager_admin.update({
                'body_html': """ Seller has rejected the membership."""
            })

            msg_vals_manager_seller.update({
                'subject': 'Membership Rejection',
                'email_to': sale.email_from,
            })
            msg_id_manager_seller = self.env['mail.mail'].create(msg_vals_manager_seller)
            msg_id_manager_seller.send()

            msg_vals_manager_admin.update({
                'subject': 'Membership Rejection',
                'email_to': 'admin@sophiesgarden.be',
            })
            msg_id_manager_admin = self.env['mail.mail'].create(msg_vals_manager_admin)
            msg_id_manager_admin.send()

            return request.redirect('/my/home')