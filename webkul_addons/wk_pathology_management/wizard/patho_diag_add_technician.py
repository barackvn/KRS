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

from odoo import models,fields,api,_
import logging
from lxml import etree
_logger = logging.getLogger(__name__)

class PathoAddTechnician(models.TransientModel):
    _name ="pathology.addtechnician"
    _description = "Pathology Add technician"

    technician = fields.Many2one('res.partner')
    add_comment= fields.Text(string="")

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(PathoAddTechnician, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        obj = self.env['patho.testreport'].browse(self._context.get('active_ids'))
        doc = etree.XML(res['arch'])
        for node in doc.xpath("//field[@name='technician']"):
            node.set(
                'domain', "[('technician','=',True),('collection_center_id', '=', %s)]" % obj.collection_center_id.id)
        res['arch'] = etree.tostring(doc)
        return res

    
    def button_addtechnician(self):
        obj = self.env['patho.testreport'].browse(self._context.get('active_ids'))
        for record in obj:
            record.lab_technician =  self.technician
            record.comment =  self.add_comment
            record.write({'diagnosis_states': 'sample_received'})
            record.compute_delivery_date()
        return True
