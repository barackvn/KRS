import re
import base64
import datetime

from odoo import fields, models, api, _, tools
from odoo.addons.iap import jsonrpc
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
import logging

_logger = logging.getLogger(__name__)


class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    vat_no_match = fields.Boolean("Is the VAT number matching?")
    address_match = fields.Boolean("Is the address matching?")
    specialisation_match = fields.Boolean("Is the specialisation matching?")
    information_match = fields.Boolean("Is there a website to get some additional information?")
    website_info_url = fields.Char("Website URL")
    match_profile = fields.Boolean("Is the seller matching with the profile?")
    reason = fields.Text("Reason")
    email_notify = fields.Boolean("Email Notify")
    assign_membership = fields.Many2one('product.template','Assign Membership Plan')


    def action_reject_profile(self):
        for record in self:
            if not record.reason:
                raise UserError(_("Please put a reason for the Rejection."))
            if record.partner_id.seller:
                mail_templ_id = self.env['ir.model.data'].get_object_reference(
                    'custom', 'template_reject_register_seller')[1]
            else:
                mail_templ_id = self.env['ir.model.data'].get_object_reference(
                    'custom', 'template_reject_register_buyer')[1]
            template_obj = self.env['mail.template'].browse(mail_templ_id)
            send = template_obj.with_context(company=self.env.company).send_mail(record.id, True)
            stage = self.env['crm.stage'].sudo().search([('name', '=', 'Rejected')])
            if not stage:
                raise UserError(_("There is no stage called Rejected in Crm Lead,Can you please create the stage."))
            record.stage_id = stage.id
            record.email_notify = True

    def action_accept_lead(self):
        for record in self:
            if record.partner_id.seller:
                # if record.partner_id.state != 'approved':
                #     raise UserError(_("Please first approved the seller profile."))
                mail_templ_id = self.env['ir.model.data'].get_object_reference(
                    'custom', 'template_accept_register_seller')[1]
                base_url = self.env['ir.config_parameter'].get_param('web.base.url')
                base_url += '/web#id=%d&view_type=form&model=%s' % (record.partner_id.id, record.partner_id._name)
                print(base_url)
                template_obj = self.env['mail.template'].browse(mail_templ_id)
                send = template_obj.with_context(company=self.env.company,url=base_url).send_mail(record.id, True)
                stage=self.env['crm.stage'].sudo().search([('name','=','Qualified')])
                if not stage:
                    raise UserError(_("There is no stage called Qualified in Crm Lead,Can you please create the stage."))
                record.stage_id=stage.id
                record.email_notify = True
            else:
                mail_templ_id = self.env['ir.model.data'].get_object_reference(
                    'custom', 'template_accept_register_buyer')[1]
                template_obj = self.env['mail.template'].browse(mail_templ_id)
                send = template_obj.with_context(company=self.env.company).send_mail(record.id, True)
                stage = self.env['crm.stage'].sudo().search([('name', '=', 'Qualified')])
                if not stage:
                    raise UserError(
                        _("There is no stage called Qualified in Crm Lead,Can you please create the stage."))
                record.stage_id = stage.id
                record.email_notify = True

            

