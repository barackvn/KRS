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

from odoo import models,fields,api
from odoo import tools
import logging
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

class DiagConfirmObtVal(models.TransientModel):
    _name= "pathology.confirm.obtval"
    _description = "Pathology Confirm Obtained Value"

    testreport_lines = fields.Many2many('patho.testreport.lines', 'patho_confirm_obtval_test_report_rel',
        'confirm_obtval_id', 'testreport_id', string="Confirm Test Report Lines")

    @api.model
    def create(self, vals):
        if vals.get('testreport_lines'):
            vals['testreport_lines'] = [(6, 0, vals.get('testreport_lines'))]
        res = super(DiagConfirmObtVal, self).create(vals)
        return res

    
    def but_confirm_diag_obtval(self):
        obj = self.env['patho.testreport'].browse(self._context.get('active_ids'))
        for record in obj.testreport_lines:
            record.testreport_lines = [(6, 0, self.testreport_lines.ids)]
            obj.write({'diagnosis_states': 'done'})

        # Make Test Request State Done if all the corresponding Diagnosis are done
        testreq_obj = self.env['patho.testrequest'].sudo().browse(obj.testreq_id.id)
        if all(status.diagnosis_states == 'done' for status in testreq_obj.patho_test_report_ids):
            testreq_obj.status = 'done'

        return True


class DiagObtVal(models.TransientModel):
    _name="pathology.obtval"
    _description = "Pathology Obtained Value"

    testreport_lines = fields.Many2many('patho.testreport.lines', 'patho_obtval_test_report_rel',
        'obtval_id', 'testreport_id', string="Test Report Lines")
    confirm = fields.Boolean("Confirm Obt Value")

    @api.model
    def create(self, vals):
        if vals.get('testreport_lines'):
            vals['testreport_lines'] = [(6, 0, vals.get('testreport_lines'))]
        res = super(DiagObtVal, self).create(vals)
        return res

    
    def but_diag_obtval(self):
        flag = 0
        for line in self.testreport_lines:
            if line.obt_val == 0.0:
                flag = 1
        if flag == 1:
            vals= {
                    'name'      :  "Confirm",
                    'view_mode' : 'form',
                    'view_type' : 'form',
                    'res_model' : 'pathology.confirm.obtval',
                    'res_id'    :  self.env['pathology.confirm.obtval'].id,
                    'context'   :  self._context,
                    'type'      : "ir.actions.act_window",
                    'target'    : 'new',
                 }
            return vals
        else:
            obj = self.env['patho.testreport'].browse(self._context.get('active_ids'))
            for record in obj.testreport_lines:
                record.testreport_lines = [(6, 0, self.testreport_lines.ids)]
                obj.write({'diagnosis_states': 'done'})

            # Make Test Request State Done if all the corresponding Diagnosis are done
            testreq_obj = self.env['patho.testrequest'].sudo().browse(obj.testreq_id.id)
            if all(status.diagnosis_states == 'done' for status in testreq_obj.patho_test_report_ids):
                testreq_obj.status = 'done'
        return True

class DiagWriteObtVal(models.TransientModel):
    _name="pathology.write.obtval"
    _description = "Pathology Write Obtained Value"

    obtained_value = fields.Float( required=True)
    test_desc = fields.Text("Description")
    test_unit = fields.Many2one(comodel_name="patho.lab.testunit" , string="Unit")
    test_min_value = fields.Float(string="Minimum Value",required=True)
    test_max_value = fields.Float(string="Maximum Value",required=True)
    test_normal_value = fields.Float(string="Normal Value",required=True)

    
    def but_diag_write_obtval(self):
        obj = self.env['patho.testreport.lines'].browse(self._context.get('active_ids'))
        for record in obj:
            record.test_min_value = self.test_min_value
            record.test_max_value = self.test_max_value
            record.test_normal_value = self.test_normal_value
            record.test_unit = self.test_unit.id
            record.obt_val = self.obtained_value
            record.test_desc = self.test_desc
        return True
