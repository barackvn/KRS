import re
import base64
import datetime

from odoo import fields, models, api, _, tools
from odoo.addons.iap import jsonrpc
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
import logging
from odoo import SUPERUSER_ID
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class SnailmailLetterInherit(models.Model):
    _inherit = 'snailmail.letter'


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # type = fields.Selection([
    # ('product', 'Item'),
    # ], string='Product Type', default='product', required=True,
    # help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
    # 'A consumable product is a product for which stock is not managed.\n'
    # 'A service is a non-material product you provide.')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    lead_id=fields.Many2one('crm.lead','Lead')
    assign_membership = fields.Many2one(related='lead_id.assign_membership', string='Assign Membership Plan')
    certification_attachment = fields.Binary("Attached Certificate")
    certificate_name = fields.Char(string="File Name", track_visibility="onchange")
    certificate_start_date = fields.Date("Certificate Start Date")
    certificate_end_date = fields.Date("Certificate End Date")

    @api.model
    def create(self, vals):
        _logger.info(">>>>>>>>>>>>>> I am in create>>>%s>>>", self)
        res = super(ResPartner, self).create(vals)
        if res:
            _logger.info(">>>>>>>>>>>>>> I am in create2>>>%s>>>", res)
            if not self._context.get('is_seller'):
                mail_templ_id = self.env['ir.model.data'].get_object_reference(
                    'custom', 'template_thnk_register_buyer')[1]
                template_obj = self.env['mail.template'].browse(mail_templ_id)
                send = template_obj.with_context(company=res.env.company).send_mail(res.id, True)
                _logger.info(">>>>>>>>>>>>>> buyer Mail send for thank you>>>%s>>>", send)
                if not res.lead_id:
                    res.create_crm_lead()
            if self._context.get('is_seller'):
                if res.seller and res.state=='new' and not res.lead_id:
                    res.sudo().set_to_pending()
                    _logger.info(">>>>>>>>>>>>>> I have update in create2>>>%s>>>", res)
                mail_templ_id = self.env['ir.model.data'].get_object_reference(
                    'custom', 'template_thnk_register_seller')[1]
                template_obj = self.env['mail.template'].browse(mail_templ_id)
                send = template_obj.with_context(company=res.env.company).send_mail(res.id, True)
                _logger.info(">>>>>>>>>>>>>> seller Mail send for thank you>>>%s>>>", send)

        return res

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        _logger.info(">>>>>>>>>>>>>> write>>>%s>>>%s", self.state,self.seller)
        if self.seller and self.state=='new' and not self.lead_id:
            self.sudo().set_to_pending()

    def create_crm_lead(self):
        if self._context.get('is_seller'):
            crm_lead = self.env['crm.lead'].sudo().create(
                {'name': self.name + ' (Seller)', 'partner_id': self.id, 'email_from': self.email, 'phone': self.phone})
        else:
            crm_lead = self.env['crm.lead'].sudo().create(
                {'name': self.name + ' (Buyer)', 'partner_id': self.id, 'email_from': self.email, 'phone': self.phone})
        self.lead_id = crm_lead.id
        if crm_lead:
            values = {
                'team_id': crm_lead.team_id.id,
            }
            if crm_lead.partner_id:
                values['partner_id'] = crm_lead.partner_id.id
            leads = crm_lead
            values.update({'lead_ids': leads.ids, 'user_ids': [crm_lead.user_id.id]})
            res = False
            leads = self.env['crm.lead'].browse(values.get('lead_ids'))
            for lead in leads:
                # self_def_user = self.with_context(default_user_id=self.user_id.id)
                # action == 'each_exist_or_create'
                # partner_id = self_def_user._create_partner(
                #     lead.id, action, values.get('partner_id') or lead.partner_id.id)
                lead.convert_opportunity(self.id, [], False)
            user_ids = values.get('user_ids')
            leads_to_allocate = leads
            if self._context.get('no_force_assignation'):
                leads_to_allocate = leads_to_allocate.filtered(lambda lead: not lead.user_id)
            if user_ids:
                leads_to_allocate.allocate_salesman(user_ids, team_id=(values.get('team_id')))
        _logger.info("~~~~~~~~create crm_lead~~~~~~~~~%r~~~~~~~~~~~~~", crm_lead)


    def set_to_pending(self):
        res_partner = super(ResPartner, self).set_to_pending()
        self.create_crm_lead()



    def approve(self):
        res_partner = super(ResPartner, self).approve()
        if self.state == "approved":
            self.enable_seller_360degree_group()
            self.enable_seller_coll_group()
            self.enable_profile_tabs_group()
            self.enable_seller_mass_upload_group()

    def action_reset_password_from_seller(self):
        for record in self:
            if record:
                for user in record.user_ids:
                    mailsend = user.sudo().action_reset_password()
                    _logger.info(">>>>>>>>>>>>>> Mail send for user reset>>>%s>>>", mailsend)

    def scheduler_seller_certificate_expiry_notify(self):
        notify_date=datetime.date.today() + relativedelta(days=14)
        seller_ids= self.env['res.partner'].search([('seller','=',True),('certificate_end_date','=',notify_date)])
        for record in seller_ids:
            if seller_ids:
                mail_templ_id = self.env['ir.model.data'].get_object_reference(
                    'custom', 'template_seller_certification_exp')[1]
                template_obj = self.env['mail.template'].browse(mail_templ_id)
                send = template_obj.with_context(company=record.env.company).send_mail(record.id, True)
                _logger.info(">>>>>>>>>>>>>> buyer Mail send for thank you>>>%s>>>", send)
