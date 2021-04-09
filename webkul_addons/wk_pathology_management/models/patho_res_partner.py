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
from dateutil.relativedelta import relativedelta
from datetime import date,datetime
from ast import literal_eval
import logging
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit="res.partner"

    patient_dob = fields.Date( string="Date Of Birth", help="Enter the date Of Birth of Patient.")
    age = fields.Char(string="Age",compute="compute_age",readonly=True,help="Computes age from DOB.")
    gender = fields.Selection([('male','Male'),('female','Female'),('others','Others')],
        string="Gender",
        help="Set whether the patient is male or female."
    )
    blood_group= fields.Selection([
        ('a','A'),
        ('b','B'),
        ('ab','AB'),
        ('o','O')], string= "Blood Group")
    rh_factor = fields.Selection([('positive','Positive(+)'), ('negative', 'Negative(-)')], string="RH Factor")
    patient = fields.Boolean( string='Is a Patient', help="Check this box if this contact is a Patient.")
    technician = fields.Boolean( string="Is a Technicial", help="Check this if this partner is a Technician.")
    pathologist = fields.Boolean( string="Is a Pathologist", help="Check this if this partner is a Pathologist.")
    tech_diagnosis_ids = fields.One2many('patho.testreport', 'lab_technician', "Technician Diagnosis Records")
    patient_testreq_ids = fields.One2many('patho.testrequest', 'customer_id', "Pathologist Diagnosis Records")
    lab_center_id = fields.Many2one('patho.lab.centers','Laboratory Center', domain="[('is_lab_center','=', True)]")
    collection_center_id = fields.Many2one('patho.lab.centers', 'Collection Center',
        domain="[('is_collection_center','=', True)]")
    patho_user_count = fields.Integer("User Count", compute="_compute_user_len")


    def _compute_user_len(self):
        for rec in self:
            rec.patho_user_count = len(rec.user_ids) if rec.user_ids else 0
        return

    @api.onchange('collection_center_id')
    def compute_lab_center(self):
        if self.collection_center_id:
            self.lab_center_id = self.collection_center_id.primary_labcenter_id.id


    def action_view_current_patho_user(self):
        users = self.mapped('user_ids')
        action = self.env.ref('base.action_res_users').read()[0]
        if len(users) > 1:
            action['domain'] = [('id', 'in', users.ids)]
        elif len(users) == 1:
            action['views'] = [(self.env.ref('base.view_users_form').id, 'form')]
            action['res_id'] = users.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action


    @api.onchange('patient_dob')
    def compute_age(self):
        for rec in self:
            if rec.patient_dob:
                dt = rec.patient_dob
                d1 = datetime.strptime(str(dt),"%Y-%m-%d").date()
                d2 = date.today()
                rd = relativedelta(d2,d1)
                rec.age = str(rd.years)+' Years '+str(rd.months)+' Months '+str(rd.days)+' Days '

    @api.onchange('patient_dob')
    def compute_dob(self):
        for rec in self:
            if rec.patient_dob:
                dt = rec.patient_dob
                d1 = datetime.strptime(str(dt),"%Y-%m-%d").date()
                d2 = date.today()
                rd = relativedelta(d2,d1)
                if rd.days < 0 or rd.months < 0 or rd.years < 0:
                    raise UserError("Date Of Birth Should be before Today")

    @api.model
    def create(self,vals):
        newpatient = super(ResPartner,self).create(vals)
        newpatient.compute_dob()
        return newpatient

    def patho_generate_user_login(self):
        for rec in self:
            if not rec.email:
                raise UserError("Please enter the email for sending Invitation")
            # assign group to this partner
            user_group = False
            technician_group = self.env['ir.model.data'].get_object_reference('wk_pathology_management', 'patho_mgmt_technician_group')[1]
            pathologist_group = self.env['ir.model.data'].get_object_reference('wk_pathology_management', 'patho_mgmt_pathologist_group')[1]
            if technician_group and pathologist_group:
                user_group = self.env["res.groups"].browse(pathologist_group if rec.pathologist else technician_group)

            # create new user
            user_vals = {
                'name': rec.name,
                'login': rec.email,
                'partner_id': rec.id,
                'company_id': self.env.company.id,
                'company_ids':[(4, self.env.company.id)],
                'groups_id':[(6,0,[user_group.id])],
            }          
            IrConfigParam = self.env['ir.config_parameter']
            template_user_id = literal_eval(IrConfigParam.get_param('base.template_portal_user_id', 'False'))
            template_user = self.env['res.users'].browse(template_user_id)
            assert template_user.exists(), 'Signup: invalid template user'

            user_vals['active'] = True
            try:
                new_user = template_user.with_context(no_reset_password=True).copy(user_vals)
                new_user.action_reset_password()
            except Exception as e:
                raise UserError(_("Error :- \n" + str(e)))

        wizard_id = self.env['patho.user.wizard'].create({'message': _("Congratulations..!! " + new_user.name + " user has been successfully created & an Invitation link has been sent to the user."), 'user_id': new_user.id})
        return {
            'name': _("Message"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'patho.user.wizard',
            'res_id': wizard_id.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new'
        }
