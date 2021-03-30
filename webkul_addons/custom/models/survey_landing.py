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

class CompanyCertificateTree(models.Model):
    _name = 'company.certificate.tree'

    info_seller = fields.Binary('Information from Seller')
    filename = fields.Char(string="File Name", track_visibility="onchange")
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    certificate_id = fields.Many2one('survey.landing', 'Certificate')

class SliderImageTree(models.Model):
    _name = 'slider.image.tree'

    preferred_link = fields.Char('Preferred Website Link')
    slider_image_file = fields.Binary('Slider Image')
    slider_id = fields.Many2one('survey.landing', 'Slider Image')

class ExtraClassM2M(models.Model):
    _name = 'extra.class.m2m'



class ProductImageTree(models.Model):
    _name = 'product.image.tree'

    product_name = fields.Char('Product Name')
    picture_html = fields.Binary('Picture')
    product_image_id = fields.Many2one('survey.landing', 'Product Image')

class SurveyLanding(models.Model):
    _name = 'survey.landing'

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
    year_starting_business = fields.Char('Year')
    tag_line_company = fields.Char("Tag Line Company")
    description_company = fields.Char("Description Company")
    certificate = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Status', default='yes')
    certificate_ids = fields.One2many('company.certificate.tree', 'certificate_id', 'Certificate1')
    company_logo = fields.Many2many(comodel_name='ir.attachment', string='')
    attachment_ids = fields.Many2many('ir.attachment', 'email_template_attachment_rels', 'email_template_ids',
                                      'attachment_id', 'Attachments')
    slider_image = fields.One2many('slider.image.tree','slider_id', 'Slider Image')
    product_image = fields.One2many('product.image.tree','product_image_id', 'Product Image')
    state = fields.Selection([('draft', 'Draft'), ('pending', 'Pending For Approval'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancelled', 'Cancelled')], string='Status', default='draft')

    def action_confirm(self):
        for record in self:
            record.write({'state': 'confirm'})

    def action_done(self):
        for record in self:
            record.write({'state': 'done'})
