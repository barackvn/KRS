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
import datetime
from datetime import timedelta

class PathoTestReport(models.Model):
    _name = "patho.testreport"
    _description = "Pathology Test Report"
    _inherit = ['mail.thread']

    name = fields.Char("Diagnosis Number",readonly=True, default="New")
    labtest = fields.Many2one("product.product", string="Lab Tests", required=True)
    lab_technician = fields.Many2one(comodel_name="res.partner",string="Lab Technician",
        domain="[('technician','=',True)]",track_visibility="onchange",)
    diagnosis_states = fields.Selection([
        ('draft','Draft'),
        ('sample_received','Sample Received'),
        ('processing','Processing'),
        ('done','Done')] ,
        readonly = True ,
        default = "draft",
        track_visibility="onchange",
        help="Shows the status of current test diagnosis"
    )
    testreq_id = fields.Many2one(comodel_name="patho.testrequest",string="Test Request", required=True)

    delivery_date = fields.Date(string="Report Delivery Date", track_visibility="onchange")
    collection_date = fields.Date(string="Sample Collected On", track_visibility="onchange")
    testreport_lines = fields.One2many('patho.testreport.lines', 'diagnosis_id', string="Test Report Lines", track_visibility="onchange")
    color = fields.Integer("Color")
    comment = fields.Text(string="Comments",
        track_visibility = "onchange",
        help = "Add the comments related to test result."
    )
    lab_center_id = fields.Many2one('patho.lab.centers','Laboratory Center', domain="[('is_lab_center','=', True)]", related="testreq_id.lab_center_id")
    collection_center_id = fields.Many2one('patho.lab.centers', 'Collection Center',
        domain="[('is_collection_center','=', True)]", related="testreq_id.collection_center_id")

    patient_name = fields.Char("Name", related="testreq_id.customer_id.name")
    patient_dob = fields.Date( string="Date Of Birth", help="Date Of Birth of Patient.", related="testreq_id.customer_id.patient_dob")
    age = fields.Char(string="Age",compute="compute_age",readonly=True,help="Age from DOB.", related="testreq_id.customer_id.age")
    gender = fields.Selection([('male','Male'),('female','Female'),('others','Others')],
        string="Gender",
        help="Set whether the patient is male or female.",
        related="testreq_id.customer_id.gender"
    )
    blood_group= fields.Selection([
        ('a','A'),
        ('b','B'),
        ('ab','AB'),
        ('o','O')], string= "Blood Group", related="testreq_id.customer_id.blood_group")
    rh_factor = fields.Selection([('positive','Positive(+)'), ('negative', 'Negative(-)')], string="RH Factor",
        related="testreq_id.customer_id.rh_factor")
    report_comment = fields.Text("Comment for Report")
    increase_level = fields.Html("Increase Level", translate= True, sanitize= True)
    decrease_level = fields.Html("Decrease Level", translate= True, sanitize= True)
    clinical_use = fields.Html("Clinical Use", translate= True, sanitize= True)

    @api.onchange('collection_center_id')
    def compute_lab_center(self):
        if self.collection_center_id:
            self.lab_center_id = self.collection_center_id.primary_labcenter_id.id

    
    def compute_delivery_date(self):
        current_date = fields.Date.today()
        delivery_time = self.labtest.report_delivery_time
        delivery_time_unit = self.labtest.report_delivery_time_unit
        delivery_date = fields.Date.today()
        if delivery_time_unit == 'week':
            delivery_time = delivery_time * 7
        if delivery_time == 0:
            delivery_date = delivery_date
        else:
            delivery_date = datetime.datetime.strptime(str(current_date),"%Y-%m-%d").date() + timedelta(days=delivery_time)
            delivery_date = str(delivery_date)
        self.delivery_date = delivery_date
        self.collection_date = current_date
        return True

    def create_patho_testreport_lines(self,labtest,diagnosis_id):
        for criteria in labtest.test_criteria:
            vals = {
                'diagnosis_id' :  diagnosis_id,
                'parameter_name' :  criteria.name.id ,
                'test_unit' :  criteria.unit.id ,
                'test_min_value' :  criteria.min_value,
                'test_max_value' :  criteria.max_value,
                'test_normal_value' :  criteria.normal_value,
                'obt_val'   :   0.0,
                # 'test_desc' :   criteria.desc,
            }
            self.env['patho.testreport.lines'].create(vals)
        return


    @api.model
    def create(self,vals):
        vals['name'] = self.env['ir.sequence'].next_by_code("patho.testreport")
        res = super(PathoTestReport,self).create(vals)
        test_id = vals.get('labtest') if vals.get('labtest') else False
        labtest = self.env['product.product'].browse(test_id)
        patient_gender = res.gender
        self.create_patho_testreport_lines(labtest, res.id)
        return res

    
    def get_start_diagnosis_wizard_action(self):
        view_id = self.env["pathology.addtechnician"].create({'add_comment':self.comment,'technician':self.lab_technician.id if self.lab_technician else False,})
        vals= {
                'name'      :  _("Assign Technician"),
                'view_mode' : 'form',
                'view_type' : 'form',
                'res_model' : 'pathology.addtechnician',
                'res_id'    : view_id.id,
                'type'      : "ir.actions.act_window",
                'target'    : 'new',
             }
        return vals

    def button_start_diagnosis(self):
        action = self.get_start_diagnosis_wizard_action()
        return action

    
    def button_set_to_processing(self):
        self.testreq_id.write({'status': 'inprocess'})
        self.write({'diagnosis_states': 'processing'})
        return True

    
    def get_done_wizard_action(self):
        view_id = self.env["pathology.obtval"].create({'testreport_lines': self.testreport_lines.ids})
        vals= {
                'name'      :  _("Add Obtained Value"),
                'view_mode' : 'form',
                'view_type' : 'form',
                'res_model' : 'pathology.obtval',
                'res_id'    : view_id.id,
                'type'      : "ir.actions.act_window",
                'target'    : 'new',
             }
        return vals

    
    def button_done(self):
        if self.testreport_lines:
            action = self.get_done_wizard_action()
            return action
        else:
            self.write({'diagnosis_states': 'done'})
        return True

class PathoTestReportLines(models.Model):
    _name = "patho.testreport.lines"
    _description = "Diagnosis Test Report Created"

    diagnosis_id = fields.Many2one('patho.testreport', string="Diagnosis Number")
    diag_states = fields.Selection(related='diagnosis_id.diagnosis_states')
    parameter_name = fields.Many2one('patho.test.parameters',required=True)
    test_unit = fields.Many2one(comodel_name="patho.lab.testunit" , string="Unit")
    test_min_value = fields.Float(string="Minimum Value",required=True)
    test_max_value = fields.Float(string="Maximum Value",required=True)
    test_normal_value = fields.Float(string="Normal Value",required=True)
    test_desc = fields.Char(string="Extra Info")
    obt_val = fields.Float(string="Obtained Value", required=True)

    
    def get_write_obtval_wizard_action(self):
        view_id = self.env["pathology.write.obtval"].create({
            'obtained_value': self.obt_val,
            'test_min_value' :self.test_min_value,
            'test_max_value' :self.test_max_value,
            'test_normal_value' :self.test_normal_value,
            'test_unit': self.test_unit.id,
        })
        vals= {
                'name'      :  _("Obtained Value"),
                'view_mode' : 'form',
                'view_type' : 'form',
                'res_model' : 'pathology.write.obtval',
                'res_id'    : view_id.id,
                'type'      : "ir.actions.act_window",
                'target'    : 'new',
             }
        return vals
