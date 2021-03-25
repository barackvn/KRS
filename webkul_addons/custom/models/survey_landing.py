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

