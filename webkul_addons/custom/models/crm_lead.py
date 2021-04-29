import re
import base64
import datetime

from odoo import fields, models, api, _, tools
from odoo.addons.iap import jsonrpc
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
import logging
import datetime
from dateutil.relativedelta import relativedelta

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
    qualify_date = fields.Date("Qualify Date")
    is_seller = fields.Boolean('Seller')
    is_buyer = fields.Boolean('Buyer')
    url_approve = fields.Char()
    url_reject = fields.Char()
    first_name = fields.Char('First Name')
    last_name = fields.Char('Last Name')




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
            stage = self.env['crm.stage'].sudo().search([('name', '=', 'Not Qualified')])
            if not stage:
                raise UserError(_("There is no stage called Not Qualified in Crm Lead,Can you please create the stage."))
            record.stage_id = stage.id
            record.email_notify = True
            record.qualify_date = datetime.date.today()

    def action_accept_lead(self):
        for record in self:
            if record.partner_id.seller:
                url_approve1 = record.get_base_url() + '/approve/' + str(record.id)
                url_reject1 = record.get_base_url() + '/reject/' + str(record.id)

                self.url_approve = url_approve1
                self.url_reject = url_reject1

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
                record.qualify_date = datetime.date.today()
                record.partner_id.lead_verify = True
                seller_user = self.env["res.users"].sudo().search([('partner_id', '=', record.partner_id.id)])
                if seller_user:
                    survey_group_obj = self.env.ref('custom.group_survey_access')
                    survey_group_obj.sudo().write({"users": [(4, seller_user.id, 0)]})

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
                record.qualify_date = datetime.date.today()

    def scheduler_seller_buyer_crm_loss_won(self):
        stage_id = self.env['crm.stage'].search([('name', 'ilike', 'Qualified')], limit=1)
        won_id = self.env['crm.stage'].search([('is_won', '=', True)], limit=1)
        loss_id = self.env['crm.stage'].search([('name', 'ilike', 'Loss')], limit=1)
        buyer_lead_ids = self.search([('stage_id', '=', stage_id.id), ('qualify_date', '!=', False), ('is_buyer', '=', True)])
        for lead in buyer_lead_ids:
            if lead.partner_id:
                order_id = self.env['sale.order'].search([('partner_id', '=', lead.partner_id.id)])
                if order_id:
                    lead.write({'stage_id': won_id.id})
                else:
                    notify_date = lead.qualify_date + relativedelta(days=13)
                    if notify_date < datetime.date.today():
                        lead.write({'stage_id': loss_id.id})
        seller_lead_ids = self.search(
            [('stage_id', '=', stage_id.id), ('qualify_date', '!=', False), ('is_seller', '=', True)])
        for member in seller_lead_ids:
            if member:
                mermbership = self.env['seller.membership'].search([('partner_id', '=', member.partner_id.id), ('state','=', 'paid')])
                if mermbership:
                    member.write({'stage_id': won_id.id})
                else:
                    notify_date = member.qualify_date + relativedelta(days=13)
                    if notify_date < datetime.date.today():
                        member.write({'stage_id': loss_id.id})


    def send_to_approve(self):
        if self.partner_id.name and self.partner_id.email:
            mail_values = {}

            mail_values.update({
                'body_html': """
                                  <p>Dear """ + self.partner_id.name + """</p>
                                  <p>Find quotation as per your request.Kindly approve if accepted</p>
                                  <br/>
                              <button style="background-color:#875A7B;color:white; padding:5px; font-size:16px;">
                                      <a style="color:white; text-decoration:none;" href='""" + self.url_approve + """'> Approve</a></button>

                              <button style="background-color:#875A7B;color:white; padding:5px; font-size:16px;">
                                      <a style="color:white; text-decoration:none;" href='""" + self.url_reject + """'> Reject </a></button>
                              <br/>
                              <p>Thanks</p>
                                                              """
            })
            mail_values.update({
                'subject': self.partner_id.name + 'Quotation Approval',
                'email_to': self.partner_id.email,
            })
            msg_id_managaer = self.env['mail.mail'].create(mail_values)
            msg_id_managaer.send()
