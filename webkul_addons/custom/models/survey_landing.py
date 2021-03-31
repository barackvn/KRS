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

class ResPatnerChild(models.Model):
    _name = 'res.partner.child'

    first_name = fields.Char("First Name")
    last_name = fields.Char("Last Name")
    job_position = fields.Char("Job Position")
    email = fields.Char("Email")
    phone = fields.Integer("Phone")
    mobile = fields.Integer("Mobile")
    survey_id = fields.Many2one('survey.landing', 'Survey')

class CertificateType(models.Model):
    _name = 'certificate.type'

    name = fields.Char("Name")

class CompanyCertificateTree(models.Model):
    _name = 'company.certificate.tree'

    info_seller = fields.Binary('Information from Seller')
    filename = fields.Char(string="File Name", track_visibility="onchange")
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    certificate_id = fields.Many2one('survey.landing', 'Certificate')
    certification_type_id = fields.Many2one("certificate.type", "Company Certification")

class SliderImageTree(models.Model):
    _name = 'slider.image.tree'

    preferred_link = fields.Char('Preferred Website Link')
    slider_image_file = fields.Binary('Slider Image')
    filename = fields.Char(string="File Name", track_visibility="onchange")
    slider_id = fields.Many2one('survey.landing', 'Slider Image')

class ExtraClassM2M(models.Model):
    _name = 'extra.class.m2m'



class ProductImageTree(models.Model):
    _name = 'product.image.tree'

    product_name = fields.Char('Product Name')
    picture_html = fields.Binary('Picture')
    filename = fields.Char(string="File Name", track_visibility="onchange")
    product_image_id = fields.Many2one('survey.landing', 'Product Image')

class SurveyLanding(models.Model):
    _name = 'survey.landing'

    user_id = fields.Many2one(
        'res.users', string='User',
        required=True,
        index=True,
        readonly=True,
        default=lambda self: self.env.uid)
    company_id = fields.Char('Company Name')
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip')
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    vat = fields.Char(string='VAT')
    language_id = fields.Many2one('res.lang', 'Language')
    speciality_id = fields.Many2many('partner.speciality', string='Specialisation')
    seller_website = fields.Char("Company Website")
    contact_ids = fields.One2many('res.partner.child','survey_id','Contacts')
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
    year_starting_business = fields.Char('Year Of Starting Business')
    tag_line_company = fields.Char("Tag Line Company")
    description_company = fields.Text("Description Company")
    certificate = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Status', default='yes')
    certificate_ids = fields.One2many('company.certificate.tree', 'certificate_id', 'Certificate1')
    company_logo = fields.Many2many(comodel_name='ir.attachment', string='')
    attachment_ids = fields.Many2many('ir.attachment', 'email_template_attachment_rels', 'email_template_ids',
                                      'attachment_id', 'Attachments')
    slider_image = fields.One2many('slider.image.tree','slider_id', 'Slider Image')
    product_image = fields.One2many('product.image.tree','product_image_id', 'Product Image')
    state = fields.Selection([('draft', 'Draft'), ('pending', 'Pending For Approval'), ('confirm', 'Confirm'), ('done', 'Done'), ('reject', 'Rejected')], string='Status', default='draft')

    def send_to_krs(self):
        for record in self:
            record.write({'state': 'pending'})

    def action_confirm(self):
        partner_id = self.user_id.partner_id
        print(partner_id)
        partner_id.write({
                'is_invoice': self.is_invoice,
                'invoice_contact_name': self.invoice_contact_name,
                'inv_company_name': self.inv_company_name,
                'inv_street': self.inv_street,
                'inv_street2': self.inv_street2,
                'inv_zip': self.inv_zip,
                'inv_city': self.inv_city,
                'inv_state_id': self.inv_state_id.id,
                'inv_country_id': self.inv_country_id.id,
                'inv_job_position': self.inv_job_position,
                'inv_email': self.inv_email,
                'inv_phone': self.inv_phone,
                'inv_mobile': self.inv_mobile,
                'is_shipping': self.is_shipping,
                'ship_contact_name': self.ship_contact_name,
                'ship_company_name': self.ship_company_name,
                'ship_street': self.ship_street,
                'ship_street2': self.ship_street2,
                'ship_zip': self.ship_zip,
                'ship_city': self.ship_city,
                'ship_state_id': self.ship_state_id.id,
                'ship_country_id': self.ship_country_id.id,
                'ship_job_position': self.ship_job_position,
                'ship_email': self.ship_email,
                'ship_phone': self.ship_phone,
                'ship_mobile': self.ship_mobile,
                'bank': self.bank,
                'account_number': self.account_number,
                'year_starting_business': self.year_starting_business,
                'tag_line_company': self.tag_line_company,
                'description_company': self.description_company,
                'certificate': self.certificate,
                # 'certificate_ids': self.certificate_ids,
                # 'res_company_logo': self.company_logo,
                # 'attachment_ids': self.attachment_ids,
                # 'slider_image': self.slider_image,
                # 'product_image': self.product_image,
                # 'company_id': self.company_id,
                # 'street': self.street,
                # 'street2': self.street2,
                # 'city': self.city,
                # 'state_id': self.state_id,
                # 'zip': self.zip,
                # 'country_id': self.country_id,
                # 'vat': self.vat,
                # 'lang': self.language_id,
                # # 'speciality_id': record.speciality_id,
                # 'url': self.seller_website
            })
        for contact in self.contact_ids:
            res_partner = self.env['res.partner'].create({
                    'parent_id': partner_id.id,
                    'name': contact.first_name + '' + contact.last_name,
                    'function': contact.job_position,
                    'email': contact.email,
                    'phone': str(contact.phone),
                    'mobile': str(contact.mobile)
                })

    def action_reject(self):
        for record in self:
            record.write({'state': 'cancel'})