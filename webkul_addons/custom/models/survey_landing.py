import re
import base64
import datetime


from odoo import fields, models, api, _, tools
from odoo.addons.iap import jsonrpc
# from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
import logging
from odoo import SUPERUSER_ID
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

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
    certificate_id_res = fields.Many2one('res.partner', 'Res Certificate')
    certificate_id = fields.Many2one('survey.landing', 'Certificate')
    certification_type_id = fields.Many2one("certificate.type", "Company Certification")

# class SliderImageTree(models.Model):
#     _name = 'slider.image.tree'
#
#     preferred_link = fields.Char('Preferred Website Link')
#     slider_image_file = fields.Binary('Slider Image')
#     filename = fields.Char(string="File Name", track_visibility="onchange")
#     slider_id = fields.Many2one('survey.landing', 'Slider Image')
#     slider_id_res = fields.Many2one('re.partner', 'Res Slider Image')

class ExtraClassM2M(models.Model):
    _name = 'extra.class.m2m'



class ProductImageTree(models.Model):
    _name = 'product.image.tree'

    brand_name = fields.Char('Brand Name')
    product_name = fields.Char('Product Name')
    net_weight = fields.Integer("Net weight")
    uom = fields.Selection([('gram','gram'),('ml','ml')], String='g/ml')
    picture_html = fields.Binary('Picture')
    filename = fields.Char(string="File Name", track_visibility="onchange")
    filename1 = fields.Char(string="File Name2", track_visibility="onchange")
    product_image_id = fields.Many2one('survey.landing', 'Product Image')
    product_hq_image = fields.Binary('HQ Image')
    product_image_id_res = fields.Many2one('res.partner', 'Res Product Image')


    @api.onchange('picture_html')
    def _onchange_picture_html(self):
        if self.picture_html:
            if str(self.filename).split('.')[-1] != 'html5':
                raise ValidationError(_("Only HTML5 files can be selected."))

class SurveyLanding(models.Model):
    _name = 'survey.landing'
    _rec_name = 'user_id'

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
    contact_ids = fields.One2many('res.partner.child', 'survey_id', 'Contacts')
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
    is_shipping = fields.Boolean("Shipping Address")
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
    # slider_image = fields.One2many('slider.image.tree','slider_id', 'Slider Image')
    slider_image = fields.Binary('Slider Image')
    filename = fields.Char(string="File Name", track_visibility="onchange")
    product_image = fields.One2many('product.image.tree','product_image_id', 'Product Image')
    state = fields.Selection([('draft', 'Draft'), ('rip', 'RIP'),('pending', 'Pending For Approval'), ('confirm', 'Done'), ('reject', 'Reject')], string='Status', default='draft')
    email_360 = fields.Boolean('Email 360')


    def action_send_product_360_image(self):
        for record in self:
            if record.user_id.partner_id.email:
                admin = self.env['res.users'].sudo().search([('id', '=', 2)])
                email = str(record.user_id.partner_id.email) + ',' + str(admin.partner_id.email)
                mail_templ_id = self.env['ir.model.data'].sudo().get_object_reference(
                    'custom', 'template_seller_for_product_360_image')[1]
                template_obj = self.env['mail.template'].browse(mail_templ_id)
                send = template_obj.with_context(company=self.env.company, email=email,
                                                 seller_name=record.user_id.partner_id.name).sudo().send_mail(record.id, True)
                record.write({'state':'rip'})

        return {
            'name': 'Email Sent',
            'domain': [],
            'res_model': 'email.sent',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {},
            'target': 'new',
        }

    def close_window(self):
        return True

    def send_to_krs(self):
        for record in self:
            # msg_vals_manager = {}
            #
            # msg_vals_manager.update({
            #     'body_html': """ Hello the seller """ + record.user_id.name + """ have saved and sent their information. """,
            #     'subject': 'SELLER ID APPROVAL',
            #     'email_from': record.user_id.email,
            #     'email_to': 'admin@sophiesgarden.be',
            # })
            #
            # msg_id_manager = self.env['mail.mail'].create(msg_vals_manager)
            # msg_id_manager.send()


            admin = self.env['res.users'].sudo().search([('id', '=', 2)])
            email = str(record.user_id.partner_id.email) + ',' + str(admin.partner_id.email)
            mail_templ_id = self.env['ir.model.data'].sudo().get_object_reference(
                    'custom', 'template_seller_send_to_kairos')[1]
            template_obj = self.env['mail.template'].browse(mail_templ_id)
            send = template_obj.with_context(company=self.env.company, email=email,seller_name=record.user_id.partner_id.name).sudo().send_mail(record.id, True)


            record.write({'state': 'pending'})

    def action_confirm(self):
        self.write({'state': 'confirm'})
        admin = self.env['res.users'].sudo().search([('id', '=', 2)])
        url_name = ''
        seller_id = self.env["res.partner"].sudo().search([('id', '=', self.user_id.partner_id.id)], limit=1)
        for record in seller_id:
            url_name = self.user_id.partner_id.name
            record.ensure_one()
            record.write({'state': 'approved'})
            if record.state == "approved":
                record.enable_seller_360degree_group()
                record.enable_seller_coll_group()
                record.enable_profile_tabs_group()
                record.enable_seller_mass_upload_group()

        email = self.user_id.partner_id.email
        msg_vals_manager = {}

        msg_vals_manager.update({
            'body_html': """ HELLO""" + str(self.user_id.partner_id.name) + """  YOUR SELLER ID FOR COMPANY """ + str(self.company_id) + """ HAS BEEN CONFIRMED! <br/>
                        You can start creating your new products through this link <a href='http://localhost:8074/web#id=&action=473&model=product.template&view_type=form&cids=1&menu_id=295'>here.</a>"""
        })
        msg_vals_manager.update({
            'subject': 'SELLER ID APPROVAL',
            'email_to': email,
        })
        msg_id_manager = self.env['mail.mail'].create(msg_vals_manager)
        msg_id_manager.send()

        if self.user_id:
            survey_group_obj = self.env.ref('custom.group_survey_access')
            survey_group_obj.sudo().write({"users": [(3, self.user_id.id, 0)]})
        partner_id = self.user_id.partner_id

        product_image_object = self.env['product.image.tree'].search([('product_image_id', '=', self.id)])
        # slider_image_object = self.env['slider.image.tree'].search([('slider_id', '=', self.id)])
        company_certification_object = self.env['company.certificate.tree'].search([('certificate_id', '=', self.id)])
        seller_shop_object = self.env['seller.banner.image'].search([('shop_id', '=', self.id)])


        for record in company_certification_object:
            partner_id.write({
                'certificate_ids': [
                    (0, 0, {
                        # 'certification_type_id': company_certification_object.certification_type_id,
                        'info_seller': record.info_seller,
                        'start_date': record.start_date,
                        'end_date': record.end_date,
                        'filename': record.filename,
                    }),
                ]
            })

        # for record in slider_image_object:
        #     partner_id.write({
        #         'slider_image': [
        #             (0, 0, {
        #                 'preferred_link': record.preferred_link,
        #                 'slider_image_file': record.slider_image_file,
        #                 'filename': record.filename,
        #             }),
        #         ]
        #     })

        for record in product_image_object:
            partner_id.write({
                'product_image': [
                    (0, 0, {
                        'brand_name': record.brand_name,
                        'net_weight': record.net_weight,
                        'uom': record.uom,
                        'product_name': record.product_name,
                        'picture_html': record.picture_html,
                        'filename': record.filename,
                        'filename1': record.filename1,
                    }),
                ]
            })
            # product_template_object = self.env['product.template'].sudo().create({
            #     'name': record.product_name,
            #     'unit_article_no': '0',
            #     'hs_code': '0',
            #     'carton_article_no': '0',
            #     'carton_barcode': '0',
            #     'conservation': 'ambient',
            #     'cust_product_category': 'solid',
            #     'ingredients': '0',
            #     'product_short_discrp': '0',
            #     'product_long_discrp': '0',
            #     'energy_kg': '0',
            #     'energy_kcal': '0',
            #     'fat': '0',
            #     'saturated_fat': '0',
            #     'mono_unsaturated_fats': '0',
            #     'poly_unsaturated_fats': '0',
            #     'carbohydrates': '0',
            #     'sugar': '0',
            #     'protein': '0',
            #     'salt': '0',
            #     'gluten_contain_grains': 'free',
            #     'milk_base_product': 'free',
            #     'eggs_base_product': 'free',
            #     'peanuts_base_product': 'free',
            #     'nuts_base_product': 'free',
            #     'soy_base_product': 'free',
            #     'mustard_base_product': 'free',
            #     'lupine_base_product': 'free',
            #     'celery_base_product': 'free',
            #     'sesame_base_product': 'free',
            #     'fish_base_product': 'free',
            #     'molluscs_base_product': 'free',
            #     'shellfish_base_product': 'free',
            #     'sulphites_base_product': 'free',
            #     'allergen_free': 'none',
            #     'antibiotic_free': 'none',
            #     'baby': 'none',
            #     'dietary': 'none',
            #     'fair_trade': 'none',
            #     'gluten_free': 'none',
            #     'gmo_free': 'none',
            #     'halal': 'none',
            #     'kosher': 'none',
            #     'lactose_free': 'none',
            #     'low_cholesterol': 'none',
            #     'low_sodium': 'none',
            #     'organic': 'none',
            #     'palm_oil_free': 'none',
            #     'paraben_free': 'none',
            #     'rich_omega': 'none',
            #     'stevia': 'none',
            #     'sugar_free': 'none',
            #     'vegan': 'none',
            #     'vegon_ok': 'none',
            #     'vegetarian': 'none',
            #     'without_preservative': 'none',
            #     'instruction': '0',
            #     'storage_instructions': '0',
            #     'serving_sug': '0',
            #     'prepare_instr': '0',
            #     'total_pallet_height': '0',
            #     'public_categ_ids': [(6, 0, 'test')],
            #     'product_tag_ids': [(6, 0, 'test')],
            #     'kind_pallet': 'test',
            #
            # })

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
                'res_company_logo': [(6, 0, self.company_logo.ids)],
                'attachment_ids': [(6, 0, self.attachment_ids.ids)],
                'description': self.description_company,
                'slider_image': self.slider_image,
                'filename': self.filename
            })




        seller_shop = self.env["seller.shop"].sudo().create({
            'name': self.company_id,
            'url_handler': url_name,
            'shop_tag_line': self.tag_line_company,
            'description': self.description_company,
            'seller_id': self.user_id.partner_id.id,
            'street': self.street,
            'street2': self.street2,
            'city': self.city,
            'state_id': self.state_id.id,
            'zip': self.zip,
            'country_id': self.country_id.id
        })
        for banner in self.attachment_ids:
            print(banner)
            if seller_shop:
                shop_banner_ids = self.env["seller.banner.image"].sudo().create({'image': banner.datas,
                 'shop_id':seller_shop.id})

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
            msg_vals_manager = {}

            msg_vals_manager.update({
                'body_html': """ Hello seller, your application for the shop has been rejected. You need to make a few changes in the application.""",
                'subject': 'SELLER ID REJECTION',
                'email_to': self.user_id.partner_id.email,
            })

            msg_id_manager = self.env['mail.mail'].create(msg_vals_manager)
            msg_id_manager.send()

            record.write({'state': 'reject'})

    @api.model
    def action_seller_shop_details(self):
        action = self.env.ref('custom.action_survey_landing').read()[0]
        if self.env.user.has_group(
                'custom.group_survey_access') and not self.env.user.has_group(
            'odoo_marketplace.marketplace_officer_group'):
            # shop_id = self.search([('seller_id', '=', self.env.user.partner_id.id)])
            landing_id = self.search([('user_id', '=', self.env.user.id)])
            if len(landing_id) > 1:
                action['domain'] = [('id', '=',landing_id.id)]
            elif len(landing_id) == 1:
                action['views'] = [(self.env.ref('custom.survey_landing_form_view').id, 'form')]
                action['res_id'] = landing_id.id
                action['domain'] = [('id', 'in', landing_id.id)]
            else:
                action['views'] = [(self.env.ref('custom.survey_landing_form_view').id, 'form')]
                action['domain'] = [('user_id', 'in', self.env.user.id)]
            return action
        else:
            action['domain'] = [('state', '!=', 'draft')]
            return action


class SellerShopInherit(models.Model):
    _inherit = 'seller.shop'

    @api.model
    def action_seller_shop(self):
        if self.env.user.has_group(
                'odoo_marketplace.marketplace_draft_seller_group') and not self.env.user.has_group(
            'odoo_marketplace.marketplace_officer_group'):
            shop_id = self.search([('seller_id', '=', self.env.user.partner_id.id)])
            action = self.env.ref('odoo_marketplace.wk_seller_shop_action').read()[0]
            if len(shop_id) > 1:
                action['domain'] = [('id', 'in', shop_id.ids)]
            elif len(shop_id) == 1:
                action['views'] = [(self.env.ref('odoo_marketplace.wk_seller_shop_form_view').id, 'form')]
                action['res_id'] = shop_id.id
            return action
        else:
            action = self.env.ref('odoo_marketplace.wk_seller_shop_action').read()[0]
            return action

class EmailSent360(models.Model):
    _name = 'email.sent'

    email_sent = fields.Char('Email Sent.', readonly=True)