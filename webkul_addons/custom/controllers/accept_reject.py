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
        sample_data = request.env['crm.lead'].sudo().search([('id', '=', int(id))], limit=1)
        stage = request.env['crm.stage'].sudo().search([('name', '=', 'Accepted')], limit=1)
        for crm in sample_data:
            crm.sudo().write({'stage_id': stage.id})

    @http.route('/reject/<string:id>', type='http', auth="user", methods=['GET', 'POST'], website=True,
                csrf=False)
    def reject_details(self, id, **post):
        sample_data = request.env['crm.lead'].sudo().search([('id', '=', int(id))], limit=1)
        stage = request.env['crm.stage'].sudo().search([('name', '=', 'Rejected')], limit=1)
        for sale in sample_data:
            sale.sudo().write({'stage_id': stage.id})
            return request.redirect('/my/home')