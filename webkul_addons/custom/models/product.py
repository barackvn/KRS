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

    product_minimum_qty = fields.Float(relative='product_tmpl_id.product_minimum_qty', string="Minimum On Hand Qty")


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    purchase_price_carton_excl_vat = fields.Monetary("Purchase price carton for buyer excl. VAT")
    purchase_price_unit_excl_vat = fields.Monetary("Purchase price per unit excl. VAT")
    adv_sale_price_excl_vat = fields.Monetary("Advisable sales price excl. VAT")
    krs_margin = fields.Float("Margin for your buyer")
    purchase_price_carton_incl_vat = fields.Monetary("Purchase price carton for buyer incl. VAT")
    purchase_price_unit_incl_vat = fields.Monetary("Purchase price per unit incl. VAT")
    adv_sale_price_incl_vat = fields.Monetary("Advisable sales price incl. VAT")
    vat_seller_kairos = fields.Monetary("VAT from seller to Kairos")
    vat_buyer_kairos = fields.Monetary("VAT from Kairos to buyer")

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
    nutriscore = fields.Float("Nutriscore")
    energy_kg = fields.Float("Energy (kj)")
    cal_energy_kg = fields.Float("Calculate Energy (kj)")
    energy_kcal = fields.Float("Energy (kcal)")
    cal_energy_kcal = fields.Float("Calculate Energy (kcal)")
    fat = fields.Float("Fats")
    cal_fat = fields.Float("Fats")
    saturated_fat = fields.Float("Totally saturated fats")
    cal_saturated_fat = fields.Float("Calculate Totally saturated fats")
    mono_unsaturated_fats = fields.Float("Monounsaturated Fats")
    cal_mono_unsaturated_fats = fields.Float("Calculate Monounsaturated Fats")
    poly_unsaturated_fats = fields.Float("Polyunsaturated fats")
    cal_poly_unsaturated_fats = fields.Float("Calculate Polyunsaturated fats")
    carbohydrates = fields.Float("Carbohydrates")
    cal_carbohydrates = fields.Float("Calculate Carbohydrates")
    sugar = fields.Float("Sugars")
    cal_sugar = fields.Float("Calculate Sugars")
    protein = fields.Float("Proteins")
    cal_protein = fields.Float("Calculate Proteins")
    salt = fields.Float("Salt")
    cal_salt = fields.Float("Calculate Salt")
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
    antibiotic_free = fields.Selection([('none', 'None'), ('friendly', 'Friendly'), ('certified', 'Certified')],
                                     'Antibiotic free')
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
    accredit_package_ids = fields.Many2many("accredited.package",string= "Accreditations mentioned on packaging")
    regulatory_ids = fields.Many2many("regulatory.type", string= "Regulatory type")
    nutrition_ids = fields.Many2many("nutrition.claims", string= "Nutrition claims")
    diet_ids = fields.Many2many("diet", string= "Diet information")
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
    min_shelf_delivery = fields.Float("Minimum shelf life on consumer")
    product_use_days = fields.Float("Total product use time")
    length_unit = fields.Float("Length single unit")
    width_unit = fields.Float("Width single unit")
    height_unit = fields.Float("Height single unit")
    volume_unit = fields.Float("Volume single unit")
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
    inbound_full_pallet = fields.Float("Inbound full pallet")
    stock_full_pallet_per_month = fields.Float("Stock full pallet per month")
    inbound_first_box = fields.Float("Inbound first box")
    stock_half_pallet_per_month = fields.Float("Stock half pallet per month")
    inbound_additional_box = fields.Float("Inbound additional box")
    stock_shelf_location_per_month = fields.Float("Stock shelf location per month (100x50x50)")
    max_cases_volume_full_box = fields.Float("Max cases on volume of the full box")
    cost_sending_per_single_unit = fields.Float("Cost sending per single unit")
    max_cases_weight_transport = fields.Float("Max cases on weight of transport")
    cost_sending_per_case = fields.Float("Cost sending per case")
    max_cases_by_weight_volume = fields.Float("Max cases by weight and volume")
    cost_sending_per_full_box = fields.Float("Cost sending per full box")
    used_box_volume = fields.Float("Used box volume")
    cost_full_box = fields.Float("Cost full box")
    percentage_cost_case = fields.Float("Percentage cost on case")
    reserve_full_box = fields.Float("Reserve full box")
    cost_effective_x_purchase = fields.Float("Cost effective from x purchase")
    margin_per_box = fields.Float("Margin per box")
    box_length = fields.Float("Box length")
    box_width = fields.Float("Box width")
    box_height = fields.Float("Box height")
    box_maximum_weight = fields.Float("Box maximum weight")

    @api.onchange('energy_kg')
    def _onchange_get_cal_energy_kg(self):
        for record in self:
            if record.energy_kg:
                record.cal_energy_kg = record.energy_kg/8400*100

    @api.onchange('energy_kcal')
    def _onchange_get_cal_energy_kcal(self):
        for record in self:
            if record.energy_kcal:
                record.cal_energy_kcal = record.energy_kcal / 2000 * 100


    @api.onchange('fat')
    def _onchange_get_cal_fat(self):
        for record in self:
            if record.fat:
                record.cal_fat = record.fat / 70 * 100


    @api.onchange('saturated_fat')
    def _onchange_get_cal_saturated_fat(self):
        for record in self:
            if record.saturated_fat:
                record.cal_saturated_fat = record.saturated_fat / 20 * 100

    @api.onchange('carbohydrates')
    def _onchange_get_cal_carbohydrates(self):
        for record in self:
            if record.carbohydrates:
                record.cal_carbohydrates = record.carbohydrates / 260 * 100

    @api.onchange('sugar')
    def _onchange_get_cal_sugar(self):
        for record in self:
            if record.sugar:
                record.cal_sugar = record.sugar / 90 * 100

    @api.onchange('protein')
    def _onchange_get_cal_protein(self):
        for record in self:
            if record.protein:
                record.cal_protein = record.protein / 50 * 100

    @api.onchange('salt')
    def _onchange_get_cal_salt(self):
        for record in self:
            if record.salt:
                record.cal_protein = record.salt / 6 * 100




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
