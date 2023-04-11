# -*- coding: utf-8 -*-
#################################################################################
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
#################################################################################

from odoo import http
from odoo.http import request
import os,zipfile,base64,io,csv
import ast
import logging
_logger = logging.getLogger(__name__)


class MarketplaceMassUpload(http.Controller):

    @http.route('/download/sample/product/zip', auth='public', website=True, type="http")
    def downloadSampleProductZip(self, **post):

        try:
            field_list,bool_value = request.env['mass.product.upload'].get_fields_name()
            bin_field_data = ','.join(field_list)
            
            buff = io.BytesIO()
            archive = zipfile.ZipFile(buff,'w',zipfile.ZIP_DEFLATED)
            archive.writestr('images/', '')
            archive.writestr('sample.csv',bytes(bin_field_data,encoding="utf-8"))
            archive.close()
            buff.flush()
            ret_zip = buff.getvalue()
            buff.close()

            return request.make_response(ret_zip,[('Content-Type', 'application/zip'),('Content-Disposition', 'attachment; filename=sample.zip')])
        except Exception as e:
            _logger.info("=========Exception===============%r",e)
            return request.render('website.page_404')


    @http.route(['/download/sample/csv','/download/sample/csv/<rec_ids>'], auth='public',website=True,type="http")
    def downloadSampleInventoryCSV(self,rec_ids=None, **post):
        
        csv_content = 'variant_id,default_code,quantity'
        if rec_ids:
            int_ids = ast.literal_eval(rec_ids)
            records = request.env['product.product'].browse(int_ids)
            list_dict_rec = []
            for rec in records:
                csv_content += f'\n{rec.id},{rec.default_code},'

        return request.make_response(csv_content,[('Content-Type', 'application/octet-stream'),('Content-Disposition', 'attachment; filename=sample.csv')])
