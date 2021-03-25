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

class PartnerSpeciality(models.Model):
    _inherit = 'partner.speciality'

    type = fields.Selection([('buyer', 'Buyer'), ('seller', 'Seller')])


class ResPartner(models.Model):
    _inherit = 'res.partner'

    lead_id=fields.Many2one('crm.lead','Lead')
    assign_membership = fields.Many2one(related='lead_id.assign_membership', string='Assign Membership Plan')
    certification_attachment = fields.Many2many(comodel_name='ir.attachment', string='Attached Certificate')
    certificate_name = fields.Char(string="File Name", track_visibility="onchange")
    certificate_start_date = fields.Date("Certificate Start Date")
    certificate_end_date = fields.Date("Certificate End Date")
    seller_location_id = fields.Many2one("stock.location","Seller Location")
    lead_verify = fields.Boolean("Lead Verified")

    def action_create_seller_location(self):
        if not self.seller_location_id:
            parent_location = self.env['stock.location'].sudo().search([('name', '=', 'WH')], limit=1)
            if parent_location:
                location=self.env['stock.location'].sudo().create({'name': self.name, 'location_id': parent_location.id, 'usage': 'internal', 'seller_id': self.id})
                self.seller_location_id = location.id

    def verify_seller_lead(self):
        leads = self.mapped('lead_id')
        action = self.env.ref('crm.crm_lead_action_pipeline').read()[0]
        form_view = [(self.env.ref('crm.crm_lead_view_form').id, 'form')]
        if 'views' in action:
            action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
        else:
            action['views'] = form_view
        action['res_id'] = leads.id
        return action
    #     if self.lead_id:
    #         return {
    #             'name': _('Package Details'),
    #             'type': 'ir.actions.act_window',
    #             'view_mode': 'form',
    #             'res_model': 'choose.delivery.package',
    #             'view_id': self.lead_id,
    #             'views': [(view_id, 'form')],
    #         }
    #
    # def action_view_invoice(self):
    #     invoices = self.mapped('invoice_ids')
    #     action = self.env.ref('crm.crm_lead_action_pipeline').read()[0]
    #     if len(invoices) > 1:
    #         action['domain'] = [('id', 'in', invoices.ids)]
    #     elif len(invoices) == 1:
    #         form_view = [(self.env.ref('account.view_move_form').id, 'form')]
    #         if 'views' in action:
    #             action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
    #         else:
    #             action['views'] = form_view
    #         action['res_id'] = invoices.id
    #     else:
    #         action = {'type': 'ir.actions.act_window_close'}
    #
    #     context = {
    #         'default_type': 'out_invoice',
    #     }
    #     if len(self) == 1:
    #         context.update({
    #             'default_partner_id': self.partner_id.id,
    #             'default_partner_shipping_id': self.partner_shipping_id.id,
    #             'default_invoice_payment_term_id': self.payment_term_id.id or self.partner_id.property_payment_term_id.id or self.env['account.move'].default_get(['invoice_payment_term_id']).get('invoice_payment_term_id'),
    #             'default_invoice_origin': self.mapped('name'),
    #             'default_user_id': self.user_id.id,
    #         })
    #     action['context'] = context
    #     return action


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
                    res.with_context(default_is_buyer=True).create_crm_lead()
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
        self.with_context(default_is_seller=True).create_crm_lead()



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
