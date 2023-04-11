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
_calender_time=[('12', '12:00am'), ('12_30', '12:30am'), ('01', '01:00am'), ('01_30', '01:30am'), ('02', '02:00am'),
         ('02_30', '02:30am'), ('03', '03:00am'), ('03_30', '03:30am'), ('04', '04:00am'), ('04_30', '04:30am'),
         ('05', '05:00am'), ('05_30', '05:30am'), ('06', '06:00am'), ('06_30', '06:30am'), ('07', '07:00am'),
         ('07_30', '07:30am'), ('08', '08:00am'), ('08_30', '08:30am'), ('09', '09:00am'), ('09_30', '09:30am'),
         ('10', '10:00am'), ('10_30', '10:30am'), ('11', '11:00am'), ('11_30', '11:30am'), ('12_p', '12:00pm'),
         ('12_30_p', '12:30pm'), ('01_p', '01:00pm'), ('01_30_p', '01:30pm'), ('02_p', '02:00pm'),
         ('02_30_p', '02:30pm'), ('03_p', '03:00pm'), ('03_30_p', '03:30pm'), ('04_p', '04:00pm'),
         ('04_30_p', '04:30pm'), ('05_p', '05:00pm'), ('05_30_p', '05:30pm'), ('06_p', '06:00pm'),
         ('06_30_p', '06:30pm'), ('07_p', '07:00pm'), ('07_30_p', '07:30pm'), ('08_p', '08:00pm'),
         ('08_30_p', '08:30pm'), ('09_p', '09:00pm'), ('09_30_p', '09:30pm'), ('10_p', '10:00pm'),
         ('10_30_p', '10:30pm'), ('11_p', '11:00pm'), ('11_30_p', '11:30pm')]


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


    membership_date = fields.Date("Membership valid until")
    country_code_ph = fields.Char(" ")
    country_code_mo = fields.Char(" ")
    lead_id = fields.Many2one('crm.lead', 'Lead')
    assign_membership = fields.Many2one(related='lead_id.assign_membership', string='Assign Membership Plan')
    certification_attachment = fields.Many2many(comodel_name='ir.attachment', string='Attached Certificate')
    certificate_name = fields.Char(string="File Name", track_visibility="onchange")
    certificate_start_date = fields.Date("Certificate Start Date")
    certificate_end_date = fields.Date("Certificate End Date")
    seller_location_id = fields.Many2one("stock.location", "Seller Location")
    lead_verify = fields.Boolean("Lead Verified")
    contact_id = fields.Char("Contact ID")
    challenge = fields.Text(" ")
    start_year = fields.Date("Start year business")
    family_owned = fields.Selection([('yes', 'YES'), ('no', 'NO')], 'Family owned')
    annual_revenue = fields.Char("Annual Revenue")
    no_of_employee = fields.Integer("Number of employees")
    yr_of_exp = fields.Char("Years of experience in export")
    agreement_person_data = fields.Boolean("Agreement to store person data (GDPR)")
    birthday = fields.Date("Birthday")
    monday = fields.Boolean('M')
    tuesday = fields.Boolean('T')
    wednesday = fields.Boolean('W')
    thursday = fields.Boolean('T')
    friday = fields.Boolean('F')
    saturday = fields.Boolean('S')
    sunday = fields.Boolean('S')
    monday_from = fields.Selection(selection=_calender_time, String="Monday")
    monday_to = fields.Selection(selection=_calender_time, String="Monday")
    tuesday_from = fields.Selection(selection=_calender_time, String="Tuesday")
    tuesday_to = fields.Selection(selection=_calender_time, String="Tuesday")
    wednesday_from = fields.Selection(selection=_calender_time, String="Wednesday")
    wednesday_to = fields.Selection(selection=_calender_time, String="Wednesday")
    thursday_from = fields.Selection(selection=_calender_time, String="Thursday")
    thursday_to = fields.Selection(selection=_calender_time, String="Thursday")
    friday_from = fields.Selection(selection=_calender_time, String="Friday")
    friday_to = fields.Selection(selection=_calender_time, String="Friday")
    saturday_from = fields.Selection(selection=_calender_time, String="Saturday")
    saturday_to = fields.Selection(selection=_calender_time, String="Saturday")
    sunday_from = fields.Selection(selection=_calender_time, String="Sunday")
    sunday_to = fields.Selection(selection=_calender_time, String="Sunday")
    matching_tags = fields.Char("Matching Business tags")
    copy_all = fields.Boolean("Copy to all")

    # weekday = fields.Selection([('mon','M'), ('tues', 'T'), ('wed', 'W'), ('thur', 'Tuesday'), ('tues', 'Tuesday')])
    # company_id = fields.Char('Company Name')
    # street = fields.Char('Street')
    # street2 = fields.Char('Street2')
    # zip = fields.Char('Zip')
    # city = fields.Char('City')
    # state_id = fields.Many2one("res.country.state", string='State')
    # country_id = fields.Many2one('res.country', string='Country')
    # vat = fields.Char(string='VAT number')
    # language_id = fields.Many2one('res.lang', 'Language')
    # speciality_id = fields.Many2many('partner.speciality', string='Specialisation')
    # contact_ids = fields.One2many('res.partner.child', 'survey_id', 'Contacts')
    is_invoice = fields.Boolean("Invoice Address")
    invoice_contact_name = fields.Char("Contact Name")
    inv_company_name = fields.Char('Company Name')
    inv_street = fields.Char('Street')
    inv_street2 = fields.Char('Street2')
    inv_zip = fields.Char('Zip')
    inv_city = fields.Char('City')
    inv_state_id = fields.Many2one("res.country.state", string='State')
    inv_country_id = fields.Many2one('res.country', string='Country')
    inv_job_position = fields.Char("Job Position")
    inv_email = fields.Char("Email")
    inv_phone = fields.Char("Phone")
    inv_mobile = fields.Char("Mobile")
    is_shipping = fields.Boolean("shipping Address")
    ship_contact_name = fields.Char("Contact Name")
    ship_company_name = fields.Char('Company Name')
    ship_street = fields.Char('Street')
    ship_street2 = fields.Char('Street2')
    ship_zip = fields.Char('Zip')
    ship_city = fields.Char('City')
    ship_state_id = fields.Many2one("res.country.state", string='State')
    ship_country_id = fields.Many2one('res.country', string='Country')
    ship_job_position = fields.Char("Job Position")
    ship_email = fields.Char("Email")
    ship_phone = fields.Char("Phone")
    ship_mobile = fields.Char("Mobile")
    bank = fields.Char("Bank")
    account_number = fields.Char("Account Number")
    year_starting_business = fields.Char('Year')
    tag_line_company = fields.Char("Company tagline")
    description_company = fields.Char("Company Description")
    certificate = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Status', default='yes')
    certificate_ids = fields.One2many('company.certificate.tree', 'certificate_id_res', 'Certificate1')
    # res_company_logo = fields.Many2many(comodel_name='ir.attachment', string='Company Logo')
    res_company_logo = fields.Many2many('ir.attachment', 'company_logo_attachment_rel', 'res_id',
                                        'attachment_id', 'Company logo', )
    attachment_ids = fields.Many2many(
        'ir.attachment', 'res_survey_attachment_rel', 'res_id',
        'attachment_id', 'Banner image')
    # slider_image = fields.One2many('slider.image.tree', 'slider_id_res', 'Slider Image')
    slider_image = fields.Binary('Slider image')
    product_image = fields.One2many('product.image.tree', 'product_image_id_res', 'Product Image')

    description = fields.Char('Description Company')
    facebook_url = fields.Char('Facebook')
    instagram_url = fields.Char('Instagram')
    twitter_url = fields.Char('Twitter')
    linkedin_url = fields.Char('Linkedin')
    youtube_url = fields.Char('Youtube')
    accept_mail_proposal = fields.Boolean("Accept Proposal")

    state = fields.Selection([('new', 'New'), ('pending', 'Pending for Approval'), ('verifying', 'Verifying'), ('approved', 'Approved'), (
        'denied', 'Denied')], string="Seller Status", default="new", copy=False, translate=True,
                             track_visibility='onchange')
    # survey_landing_ids = fields.Many2one('res.partner')
    @api.depends('country_id')
    def _onchange_country(self):
        if self.country_id:
            self.country_code_ph = self.country_id.phone_code
            self.country_code_mo = self.country_id.phone_code


    def see_offer_button(self):
        pass

    def action_send_product_360(self):
        for record in self:
            if record.email:
                admin = self.env['res.users'].sudo().search([('id', '=', 2)])
                email = f'{str(record.email)},{str(admin.email)}'
                mail_templ_id = self.env['ir.model.data'].sudo().get_object_reference(
                    'custom', 'template_seller_for_product_360_image')[1]
                template_obj = self.env['mail.template'].browse(mail_templ_id)
                send = template_obj.with_context(company=self.env.company, email=email,
                                                 seller_name=record.name).sudo().send_mail(record.id, True)
                # record.wri.te({'state': 'rip'})

        # return {
        #     'name': 'Email Sent',
        #     'domain': [],
        #     'res_model': 'email.sent',
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     'view_type': 'form',
        #     'context': {},
        #     'target': 'new',
        # }

    def action_create_seller_location(self):
        if not self.seller_location_id:
            if (
                parent_location := self.env['stock.location']
                .sudo()
                .search([('name', '=', 'WH')], limit=1)
            ):
                location = self.env['stock.location'].sudo().create(
                    {'name': self.name, 'location_id': parent_location.id, 'usage': 'internal', 'seller_id': self.id})
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

    @api.model
    def create(self, vals):
        _logger.info(">>>>>>>>>>>>>> I am in create>>>%s>>>", self)
        res = super(ResPartner, self).create(vals)
        msg_vals_manager_seller = {}
        msg_vals_manager_buyer = {}
        if res:
            _logger.info(">>>>>>>>>>>>>> I am in create2>>>%s>>>", res)
            if not self._context.get('is_seller') and not res.parent_id:
                mail_templ_id = self.env['ir.model.data'].get_object_reference(
                    'custom', 'template_thnk_register_buyer')[1]
                template_obj = self.env['mail.template'].browse(mail_templ_id)
                send = template_obj.with_context(company=res.env.company).send_mail(res.id, True)
                _logger.info(">>>>>>>>>>>>>> buyer Mail send for thank you>>>%s>>>", send)
                if not res.lead_id:
                    res.with_context(default_is_buyer=True).create_crm_lead()
            if self._context.get('is_seller') and not res.parent_id:
                res.write({'contact_id': self.env['ir.sequence'].next_by_code('seller.contact') or ''})
                if (
                    seller_user := self.env["res.users"]
                    .sudo()
                    .search([('partner_id', '=', res.id)])
                ):
                    contact_group_obj = self.env.ref('base.group_partner_manager')
                    contact_group_obj.sudo().write({"users": [(4, seller_user.id, 0)]})
                if res.seller and res.state == 'new' and not res.lead_id:
                    res.sudo().set_to_pending()
                    _logger.info(">>>>>>>>>>>>>> I have update in create2>>>%s>>>", res)
                mail_templ_id = self.env['ir.model.data'].get_object_reference(
                    'custom', 'template_thnk_register_seller')[1]
                template_obj = self.env['mail.template'].browse(mail_templ_id)
                send = template_obj.with_context(company=res.env.company).send_mail(res.id, True)
                seller_mail_templ_id = self.env['ir.model.data'].get_object_reference(
                    'custom', 'template_register_seller')[1]
                seller_template_obj = self.env['mail.template'].browse(seller_mail_templ_id)
                seller_send = seller_template_obj.with_context(company=res.env.company).send_mail(res.id, True)
                _logger.info(">>>>>>>>>>>>>> seller Mail send for thank you>>>%s>>>", send)
        return res

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        _logger.info(">>>>>>>>>>>>>> write>>>%s>>>%s", self.state, self.seller)
        if self.seller and self.state == 'new' and not self.lead_id and not self.parent_id:
            self.sudo().set_to_pending()


    @api.onchange('monday','tuesday','wednesday','thursday','friday','saturday','sunday')
    def _onchange_delivery_time(self):
        if not self.monday:
            self.monday_from = False
            self.monday_to = False
        if not self.tuesday:
            self.tuesday_from = False
            self.tuesday_to = False
        if not self.wednesday:
            self.wednesday_from = False
            self.wednesday_to = False
        if not self.thursday:
            self.thursday_from = False
            self.thursday_to = False
        if not self.friday:
            self.friday_from = False
            self.friday_to = False
        if not self.saturday:
            self.saturday_from = False
            self.saturday_to = False
        if not self.sunday:
            self.sunday_from = False
            self.sunday_to = False


    def copy_them_all(self):
        time_from = self.monday_from or self.tuesday_from or self.wednesday_from or self.thursday_from or self.friday_from or self.saturday_from or self.sunday_from
        time_to = self.monday_to or self.tuesday_to or self.wednesday_to or self.thursday_to or self.friday_to or self.saturday_to or self.sunday_to
        if self.monday:
            self.monday_from = time_from
            self.monday_to = time_to
        if self.tuesday:
            self.tuesday_from = time_from
            self.tuesday_to  = time_to
        if self.wednesday:
            self.wednesday_from = time_from
            self.wednesday_to  = time_to
        if self.thursday:
            self.thursday_from = time_from
            self.thursday_to  = time_to
        if self.friday:
            self.friday_from = time_from
            self.friday_to  = time_to
        if self.saturday:
            self.saturday_from = time_from
            self.saturday_to  = time_to
        if self.sunday:
            self.sunday_from = time_from
            self.sunday_to  = time_to

    def create_crm_lead(self):
        if self._context.get('is_seller'):
            crm_lead = (
                self.env['crm.lead']
                .sudo()
                .create(
                    {
                        'name': f'{self.name} (Seller)',
                        'partner_id': self.id,
                        'email_from': self.email,
                        'phone': self.phone,
                    }
                )
            )
        else:
            crm_lead = (
                self.env['crm.lead']
                .sudo()
                .create(
                    {
                        'name': f'{self.name} (Buyer)',
                        'partner_id': self.id,
                        'email_from': self.email,
                        'phone': self.phone,
                    }
                )
            )
        self.lead_id = crm_lead.id
        if crm_lead:
            values = {
                'team_id': crm_lead.team_id.id,
            }
            if crm_lead.partner_id:
                values['partner_id'] = crm_lead.partner_id.id
            leads = crm_lead
            values |= {'lead_ids': leads.ids, 'user_ids': [leads.user_id.id]}
            res = False
            leads = self.env['crm.lead'].sudo().browse(values.get('lead_ids'))
            for lead in leads:
                # self_def_user = self.with_context(default_user_id=self.user_id.id)
                # action == 'each_exist_or_create'
                # partner_id = self_def_user._create_partner(
                #     lead.id, action, values.get('partner_id') or lead.partner_id.id)
                lead.sudo().convert_opportunity(self.id, [], False)
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
        notify_date = datetime.date.today() + relativedelta(days=14)
        seller_ids = self.env['res.partner'].search([('seller', '=', True), ('certificate_end_date', '=', notify_date)])
        for record in seller_ids:
            if seller_ids:
                mail_templ_id = self.env['ir.model.data'].get_object_reference(
                    'custom', 'template_seller_certification_exp')[1]
                template_obj = self.env['mail.template'].browse(mail_templ_id)
                send = template_obj.with_context(company=record.env.company).send_mail(record.id, True)
                _logger.info(">>>>>>>>>>>>>> buyer Mail send for thank you>>>%s>>>", send)

class SellerMembershipInherit(models.Model):
    _inherit = 'seller.membership'

    mp_membership_date_from = fields.Date(string='Accepted date')
    mp_membership_date_to = fields.Date(string='Expire date')
    date = fields.Date(string='Date registration', help="Date on which member has requested the membership")
    mp_membership_fee = fields.Float(string='Price paid', digits='Product Price', required=True, help='Amount for the membership.')
    first_purchase_date = fields.Date(string="First purchase date")

