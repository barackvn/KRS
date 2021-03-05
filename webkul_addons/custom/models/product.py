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

class Diet(models.Model):
    _name = 'diet'

    name = fields.Char("Name")

class FishZone(models.Model):
    _name = 'fish.zone'

    name = fields.Char("Name")

class Fishing(models.Model):
    _name = 'fishing'

    name = fields.Char("Name")

class Volume(models.Model):
    _name = 'volume'

    name = fields.Char("Name")

class PalletKind(models.Model):
    _name = 'pallet.kind'

    name = fields.Char("Name")


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    # product_id = fields.Many2one("product.template","product")

class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    # product_minimum_qty = fields.Float(relative='product_tmpl_id.product_minimum_qty', string="Minimum On Hand Qty")


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    purchase_price_carton_excl_vat = fields.Float("Purchase price carton for buyer excl. VAT")
    purchase_price_unit_excl_vat = fields.Float("Purchase price per unit excl. VAT")
    adv_sale_price_excl_vat = fields.Float("Advisable sales price excl. VAT")
    krs_margin = fields.Float("Margin for your buyer")
    purchase_price_carton_incl_vat = fields.Float("Purchase price carton for buyer incl. VAT")
    purchase_price_unit_incl_vat = fields.Float("Purchase price per unit incl. VAT")
    adv_sale_price_incl_vat = fields.Float("Advisable sales price incl. VAT")
    qty_single_unit_per_cartn = fields.Float("Quantity of single per carton")
    conservation = fields.Selection([('ambient', 'Ambient'), ('fresh', 'Fresh'), ('frozen', 'Frozen')],
                                             'Conservation method')
    net_weight_single_unit = fields.Char("Net weight single unit")
    unit_barcode = fields.Char("Single unit barcode / EAN13")
    carton_barcode = fields.Char("Carton barcode / EAN14")
    unit_article_no = fields.Char("Single unit article number")
    carton_article_no = fields.Char("Carton article number")
    product_short_discrp = fields.Text("Product short description")
    product_long_discrp = fields.Text("Product Long description")
    ingredients = fields.Text("Ingredients")
    nutriscore = fields.Char("Nutriscore")
    energy_kg = fields.Float("Energy (Kg)")
    energy_kcal = fields.Float("Energy (Kcal)")
    fat = fields.Float("Fats")
    saturated_fat = fields.Float("Totally saturated fats")
    mono_unsaturated_fats = fields.Float("Monounsaturated Fats")
    poly_unsaturated_fats = fields.Float("Polyunsaturated fats")
    carbohydrates = fields.Float("Carbohydrates")
    sugar = fields.Float("Sugars")
    protein = fields.Float("Proteins")
    salt = fields.Float("Salt")
    cal_nutri_percent = fields.Float("Calculation percentage")
    gluten_contain_grains = fields.Selection([('free', 'Free'), ('may_c', 'May Contain'), ('contain', 'Contains')],
                                             'Gluten-Containing Grains')
    milk_base_product = fields.Selection([('free', 'Free'), ('may_c', 'May Contain'), ('contain', 'Contains')],
                                         'Milk and Milk-based Products')
    eggs_base_product = fields.Selection([('free', 'Free'), ('may_c', 'May Contain'), ('contain', 'Contains')],
                                         'Eggs and egg-based products')
    peanuts_base_product = fields.Selection([('free', 'Free'), ('may_c', 'May Contain'), ('contain', 'Contains')],
                                            'Peanuts (groundnuts) and peanut-based products')
    nuts_base_product = fields.Selection([('free', 'Free'), ('may_c', 'May Contain'), ('contain', 'Contains')],
                                         'Nuts and nut-based products')
    soy_base_product = fields.Selection([('free', 'Free'), ('may_c', 'May Contain'), ('contain', 'Contains')],
                                        'Soy and soy-based products')
    mustard_base_product = fields.Selection([('free', 'Free'), ('may_c', 'May Contain'), ('contain', 'Contains')],
                                            'Mustard and mustard-based products')
    lupine_base_product = fields.Selection([('free', 'Free'), ('may_c', 'May Contain'), ('contain', 'Contains')],
                                           'Lupine and lupine-based products')
    celery_base_product = fields.Selection([('free', 'Free'), ('may_c', 'May Contain'), ('contain', 'Contains')],
                                           'Celery and celery-based products')
    sesame_base_product = fields.Selection([('free', 'Free'), ('may_c', 'May Contain'), ('contain', 'Contains')],
                                           'Sesame seeds and products based on sesame seeds')
    fish_base_product = fields.Selection([('free', 'Free'), ('may_c', 'May Contain'), ('contain', 'Contains')],
                                         'Fish and fish based products')
    molluscs_base_product = fields.Selection([('free', 'Free'), ('may_c', 'May Contain'), ('contain', 'Contains')],
                                             'Molluscs and products based on molluscs')
    shellfish_base_product = fields.Selection([('free', 'Free'), ('may_c', 'May Contain'), ('contain', 'Contains')],
                                              'Crustaceans and products based on shellfish')
    sulphites_base_product = fields.Selection([('free', 'Free'), ('may_c', 'May Contain'), ('contain', 'Contains')],
                                              'Sulfur dioxide and sulphites (E220-E228)')
    allergen_free = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                     'Allergen free')
    baby = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                            'Baby')
    dietary = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                               'Dietary')
    fair_trade = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                  'Fair Trade')
    gluten_free = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                   'Gluten free')
    gmo_free = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                'GMO free')
    halal = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                             'Halal')
    kosher = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                              'Kosher')
    lactose_free = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                    'Lactose free')
    low_cholesterol = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                       'Low cholesterol')
    low_sodium = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                  'Low sodium / Sodium free')
    organic = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                               'Organic')
    palm_oil_free = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                     'Palm oil free')
    paraben_free = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                    'Paraben Free')
    rich_omega = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                  'Rich in omega 3 – 6')
    stevia = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                              'Stevia')
    sugar_free = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                  'Sugar free')
    vegan = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                             'Vegan')
    vegon_ok = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                'Vegon OK')
    vegetarian = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                  'Vegetarian')
    without_preservative = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                            'Without preservatives')
    instruction = fields.Text("Instructions for use")
    storage_instructions = fields.Text("Storage instructions")
    serving_sug = fields.Text("Serving instructions")
    prepare_instr = fields.Text("Preparation instructions")
    local_accredit_package = fields.Selection(
        [('separate', 'Separate collection'), ('nix18', 'NIX18'), ('pregnacy', 'Pregnacy logo')],
        'Local accreditations mentioned on packaging')
    accredit_package_id = fields.Many2one("accredited.package", "accreditations mentioned on packaging")
    regulatory_id = fields.Many2one("regulatory.type", "Regulatory type")
    nutrition_id = fields.Many2one("nutrition.claims", "Nutrition claims")
    diet_id = fields.Many2one("diet", "Diet information")
    place_birth = fields.Char("Place of birth")
    place_assembly = fields.Char("Place of assembly")
    place_entry = fields.Char("Place of entry")
    place_milking = fields.Char("Place of milking")
    place_fattening = fields.Char("Place of fattening")
    place_bottling = fields.Char("Place of bottling")
    place_operation = fields.Char("Place of last operation")
    place_slaughter = fields.Char("Place of slaughter")
    place_product_grown = fields.Char("Place where the product was grown")
    location_origin = fields.Selection(
        [('non_or_eu', 'EU or non-EU Agriculture'), ('eu', 'EU agriculture'), ('farming', 'Farming country of origin'),
         ('non_eu', 'Non-EU Agriculture')],
        'Location of origin')
    country_origin_id = fields.Many2one('res.country', 'Country of origin')
    region_country = fields.Char('Region of country')
    fish_zone_id = fields.Many2one('fish.zone', 'Fishing area for fish and crustaceans')
    fishing_id = fields.Many2one('fishing', 'Fishing method')
    manufacture_days = fields.Float("Manufacturing lead time")
    transport_days = fields.Float("Transport to fulfilment time")
    fulfilment_days = fields.Float("Fulfilment time", default=1.0)
    product_alert_day = fields.Float("Product alert time")
    product_removal_days = fields.Float("Product removal time")
    min_shelf_delivery = fields.Float("Minimum shelf life on delivery")
    product_use_days = fields.Float("Total product use time")
    length_unit = fields.Float("Length single unit")
    width_unit = fields.Float("Width single unit")
    height_unit = fields.Float("Height single unit")
    volume_unit = fields.Many2one("volume","Volume single unit")
    length_carton = fields.Float("Length carton")
    width_carton = fields.Float("Width carton")
    height_carton = fields.Float("Height carton")
    volume_carton = fields.Float("Volume carton")
    net_content_per_unit = fields.Float("Net content per single unit")
    drained_weight_per_unit = fields.Float("Drained weight per single unit")
    net_weight_per_unit = fields.Float("Net weight per single unit")
    gross_weight_per_unit = fields.Float("Gross weight per single unit")
    net_content_per_carton = fields.Float("Net content carton")
    drained_weight_per_carton = fields.Float("Drained weight carton")
    net_weight_per_carton = fields.Float("Net weight carton")
    gross_weight_per_carton = fields.Float("Gross weight carton")
    pallet_quantity = fields.Float("Amount of cartons on full pallet")
    kind_pallet = fields.Many2one("pallet.kind","Kind of pallet")
    total_pallet_height = fields.Char("Total full pallet height")
    per_product_ff_charge = fields.Float("Per Product FF Charge")
    product_minimum_qty = fields.Float("Minimum On Hand Qty")



    # product_place = fields.Char("Place of origin organic product")
    # origin_type = fields.Char("Type of origin")
    # method_capture = fields.Many2one("method.capture", "Method of capture")
    # area_capture = fields.Many2one("area.capture", "Area of capture")
    #
    # nutritional_info = fields.Text("Nutritional information")
    # allergens = fields.Char("Allergens")
    # pallet_length = fields.Char("Pallet Length")
    # pallet_height = fields.Char("Pallet height")





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
