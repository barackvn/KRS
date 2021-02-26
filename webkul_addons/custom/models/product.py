import re
import base64
import datetime

from odoo import fields, models, api, _, tools
from odoo.addons.iap import jsonrpc
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
import logging

_logger = logging.getLogger(__name__)

class NutritionClaims(models.Model):
    _name = 'nutrition.claims'

    name = fields.Char("Nutrition Name")

class AccreditedPackage(models.Model):
    _name = 'accredited.package'

    name = fields.Char("Name")

class RegulatoryType(models.Model):
    _name = 'regulatory.type'

    name = fields.Char("Name")

class MethodCapture(models.Model):
    _name = 'method.capture'

    name = fields.Char("Name")

class AreaCapture(models.Model):
    _name = 'area.capture'

    name = fields.Char("Name")

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    # product_id = fields.Many2one("product.template","product")


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'


    purchase_price_excl_vat = fields.Float("Purchase price excl. VAT")
    adv_sale_price_incl_vat = fields.Float("Advisable sales price incl. VAT")
    krs_margin = fields.Float("Margin")
    purchase_price_unit_excl_vat = fields.Float("Purchase price (x units) excl. VAT")
    qty_single_unit_per_cartn = fields.Float("Quantity single units per carton")
    net_weight_single_unit = fields.Char("Net weight single unit")
    carton_barcode = fields.Char("Carton barcode / EAN14")
    carton_article_no = fields.Char("Carton article number")
    product_short_discrp = fields.Text("Product short description")
    ingredients = fields.Text("Ingredients")
    nutrition_id = fields.Many2one("nutrition.claims", "Nutrition claims")
    accredit_package = fields.Many2one("accredited.package", "Local accreditations mentioned on packaging")
    regulatory_id = fields.Many2one("regulatory.type","Regulatory type")
    country_origin = fields.Char("Country of origin")
    product_place = fields.Char("Place of origin organic product")
    origin_type = fields.Char("Type of origin")
    method_capture = fields.Many2one("method.capture","Method of capture")
    area_capture = fields.Many2one("area.capture","Area of capture")
    nutriscore = fields.Char("Nutriscore")
    nutritional_info = fields.Char("Nutritional information")
    allergens = fields.Char("Allergens")
    instruction = fields.Char("Instructions for use")
    storage_instructions = fields.Char("Instructions for use")
    serving_sug = fields.Char("Serving suggestions")
    prepare_instr = fields.Char("Preparation instructions")
    net_content_per_unit = fields.Float("Net content per single unit")
    drained_weight_per_unit = fields.Float("Drained weight per single unit")
    net_weight_per_unit = fields.Float("Net weight per single unit")
    gross_weight_per_unit = fields.Float("Gross weight per single unit")
    length_unit = fields.Float("Length single unit")
    width_unit = fields.Float("Width single unit")
    height_unit = fields.Float("Height single unit")
    volume_unit = fields.Float("Volume single unit")
    net_content_per_carton = fields.Float("Net content per carton")
    drained_weight_per_carton = fields.Float("Drained weight per carton")
    net_weight_per_carton = fields.Float("Net weight per carton")
    gross_weight_per_carton = fields.Float("Gross weight per carton")
    length_carton = fields.Float("Length carton")
    width_carton = fields.Float("Width carton")
    height_carton = fields.Float("Height carton")
    length_carton = fields.Float("Length carton")
    volume_carton = fields.Float("Volume carton")
    pallet_quantity = fields.Float("Amount of cartons on a pallet")
    pallet_length = fields.Char("Pallet Length")
    pallet_height = fields.Char("Pallet height")
    manufacture_days = fields.Float("Manufacturing lead time")
    transport_days = fields.Float("Transport lead time")
    min_shelf_delivery = fields.Float("Minimum shelf life on delivery")
    product_use_days = fields.Float("Product use time")
    product_removal_days = fields.Float("Product removal time")
    alert_date = fields.Date("Alert time")
    # file_upload = fields.One2many(comodel_name='ir.attachment',inverse_name='product_id', string="File Upload")
    attachment_ids = fields.Many2many(comodel_name='ir.attachment', string='Attachments')


    @api.model
    def create(self, vals):
        res = super(ProductTemplateInherit, self).create(vals)
        if res:
            res.write({'default_code': self.env['ir.sequence'].next_by_code('internal.ref') or ''})
        return res


class SellerShopInherit(models.Model):
    _inherit = "seller.shop"

    @api.model
    def default_get(self, fields):
        rec = super(SellerShopInherit, self).default_get(fields)
        if not self._context.get("default_seller_id"):
            rec["seller_id"] = self.env.user.partner_id.id
        return rec

    user_id = fields.Many2one(
        'res.users', string='User',
        required=True,
        index=True,
        readonly=True,
        default=lambda self: self.env.uid)
