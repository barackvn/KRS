# -*- coding: utf-8 -*-
#################################################################################
##    Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


class MaintenanceMode(models.Model):
    _name = 'maintenance.mode'
    _description = "Maintenance Mode"
    name = fields.Char('Name', default='Maintenance Mode')
    page_header = fields.Char(string="Title of page",
                              help="Title of the page you want to display during the maintenance mode(in the main page on website)", translate=True)
    page_message = fields.Text(string="Message displayed in page",
                               help="Message you want to display during the maintenance mode(in the main page on website)", translate=True)
    login_message = fields.Char(string="Message at login page",
                                help="Message you want to display if an user tries to login (in the login page on website)", translate=True)
    image = fields.Binary(
        string="Image", help="Image to be displayed during maintenance mode in website")
    admin_message = fields.Char(string="Message for accessible users",
                                help="Message you want to display for accessible users in maintenance mode", translate=True)
    subscriber_email_ids = fields.One2many(
        'wk.subscriber.emails', 'maintenance_mode_id', string="Notifying Emails")
    display_email_field = fields.Boolean('Enable notification feature in website template',
                                         help="By enabling this email notification feature will be enabled in website")
    display_admin_mesage = fields.Boolean(
        'Display message to accessible users', help="Message to be displayed to accessible users in maintenance mode.")
    email_error_msg = fields.Char('Message displayed on invalid email', translate=True,
                                  help="message displayed to customers on entering an invalid email")
    email_valid_msg = fields.Char('Message displayed on valid email',
                                  help="message displayed to customers on entering a valid email", translate=True)
    email_notif_title = fields.Char('Title for email Notification ',
                                    help="Title to be displayed for email notification feature", translate=True)
    email_exists = fields.Char('Dessage displayed if email exists ',
                               help="Message displayed if the email already exists and is in the pending state", translate=True)

    
    def save(self):
        self.ensure_one()
        view_id = self.env.ref('odoo_maintenance_mode.res_config_settings_view_form_inherited_maintenance_mode').id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.config.settings',
            'view_type': 'form',
            'view_id': view_id,
            'view_mode': 'form',
            'target': 'inline',
            'context':{'module' : 'odoo_maintenance_mode'}
        }

    @api.model
    def send_email_method(self, maintenance_mode_obj):
        temp_id = self.env.ref(
            'odoo_maintenance_mode.mail_template_maintenance_mode').id
        if temp_id and maintenance_mode_obj:
            ir_model_data = self.env['ir.model.data']
            template_obj = self.env['mail.template'].browse(temp_id)
            reciepts = ''
            for mail_id in maintenance_mode_obj.subscriber_email_ids:
                if mail_id.state == 'pending':
                    reciepts += f'{mail_id.email},'
                    mail_id.state = 'sent'
            values = {'email_to': reciepts}
            template_obj.send_mail(maintenance_mode_obj.id, True, '', values)

    
    def wk_send_email_to_notifiers(self):
        maintenance_mode_id = self.env['ir.config_parameter'].get_param(
            'maintenance_mode_id')
        maintenance_mode = self.env['ir.config_parameter'].get_param(
            'maintenance_mode')
        msg = ''
        if maintenance_mode:
            msg = 'You can not send the notifications while the maintenace mode is on.'
        else:
            maintenance_mode_obj = self.browse(int(maintenance_mode_id))
            self.send_email_method(maintenance_mode_obj)
            msg = 'Mail sent successfully to the customers'
        wizard_id = self.env['wk.wizard.message'].create(
            {'text': msg})
        return {'name': _("Summary"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'wk.wizard.message',
                'res_id': wizard_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
                }


class WkSubscriberEmails(models.Model):
    _name = 'wk.subscriber.emails'
    _order = 'write_date'

    email = fields.Char('Email')
    create_date = fields.Datetime('Created Date')
    write_date = fields.Datetime('Updated On')
    state = fields.Selection(
        [('pending', 'Pending'), ('sent', 'Sent')], string="State")
    maintenance_mode_id = fields.Many2one(
        'maintenance.mode', string=" Maintenance mode")
