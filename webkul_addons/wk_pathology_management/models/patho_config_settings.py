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

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = "Pathology Configuration settings"

    lab_center_id = fields.Many2one('patho.lab.centers','Lab Center', domain="[('is_lab_center', '=', True)]")
    collection_center_id = fields.Many2one('patho.lab.centers', 'Collection Center',
        domain="[('is_collection_center', '=', True)]")
    enable_notify_reminder = fields.Boolean("Enable to send mail reminder before test")
    notify_reminder_mail_template = fields.Many2one(
        "mail.template", string="Mail Notification Reminder", domain="[('model_id.model','=','patho.testrequest')]")
    enable_notify_customer_on_approve_testreq = fields.Boolean("Enable to send mail on Test Request Confirmation")
    notify_customer_on_approve_testreq = fields.Many2one(
        "mail.template", string="Test Request Confirmation Mail", domain="[('model_id.model','=','patho.testrequest')]")

    @api.onchange('collection_center_id')
    def compute_lab_center(self):
        if self.collection_center_id:
            self.lab_center_id = self.collection_center_id.primary_labcenter_id.id

    
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrDefault = self.env['ir.default'].sudo()
        IrDefault.set('res.config.settings', 'lab_center_id', self.lab_center_id.id)
        IrDefault.set('res.config.settings', 'collection_center_id', self.collection_center_id.id)
        IrDefault.set('res.config.settings', 'enable_notify_reminder', self.enable_notify_reminder)
        IrDefault.set('res.config.settings', 'notify_reminder_mail_template', self.notify_reminder_mail_template.id)
        IrDefault.set('res.config.settings', 'enable_notify_customer_on_approve_testreq', self.enable_notify_customer_on_approve_testreq)
        IrDefault.set('res.config.settings', 'notify_customer_on_approve_testreq', self.notify_customer_on_approve_testreq.id)
        return True

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        testreq_reminder_mail_template = self.env['ir.model.data'].get_object_reference(
            'wk_pathology_management', 'patho_reminder_mail_to_customer')[1]
        notify_customer_on_approve_testreq = self.env['ir.model.data'].get_object_reference(
            'wk_pathology_management', 'patho_mgmt_email_template_to_customer')[1]
        IrDefault = self.env['ir.default'].sudo()
        res.update(
            {
            'lab_center_id':IrDefault.get('res.config.settings', 'lab_center_id'),
            'collection_center_id':IrDefault.get('res.config.settings', 'collection_center_id'),
            'enable_notify_reminder':IrDefault.get('res.config.settings', 'enable_notify_reminder'),
            'notify_reminder_mail_template':IrDefault.get('res.config.settings', 'notify_reminder_mail_template')
                or testreq_reminder_mail_template,
            'enable_notify_customer_on_approve_testreq':IrDefault.get('res.config.settings', 'enable_notify_customer_on_approve_testreq'),
            'notify_customer_on_approve_testreq':IrDefault.get('res.config.settings', 'notify_customer_on_approve_testreq')
                or notify_customer_on_approve_testreq,
            }
        )
        return res
