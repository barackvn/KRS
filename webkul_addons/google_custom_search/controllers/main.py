# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################

import base64
from odoo.addons.web.controllers.main import serialize_exception, content_disposition
from odoo import http
from odoo.http import request



class CustomSearchEngine(http.Controller):

    @http.route('/gce/download_files', type='http', auth="public")
    @serialize_exception
    def download_cse_file(self, **kw):
        """ Download link for files stored as binary fields.
        """
        IrConfigPrmtr = request.env['ir.config_parameter'].sudo()
        cseFile = IrConfigPrmtr.get_param(
            'google_custom_search.cse_file'
        )
        cseFileName = IrConfigPrmtr.get_param(
            'google_custom_search.cse_filename'
        )
        filecontent = base64.b64decode(cseFile or '')
        if not filecontent:
            return request.not_found()
        else:
            return request.make_response(filecontent,
                                        [('Content-Type', 'application/octet-stream'),
                                            ('Content-Disposition', content_disposition(cseFileName))])

    @http.route(['/get/engine_id/'], type='json', auth="public", methods=['POST'], website=True)
    def get_engine_id(self):
        IrConfigPrmtr = request.env['ir.config_parameter'].sudo()
        engineId = IrConfigPrmtr.get_param(
            'google_custom_search.cse_unique_id'
        )
        enableCSE = IrConfigPrmtr.get_param(
            'google_custom_search.cse_enable'
        )
        return {'engine_id': engineId, 'enable_cse': enableCSE}
