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


class ProductPricelistItemInherit(models.Model):
    _inherit = "product.pricelist.item"

    single_unit_carton = fields.Char("Single unit or carton")
    max_quantity = fields.Integer("Maximum quantity")

class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    product_minimum_qty = fields.Float(relative='product_tmpl_id.product_minimum_qty', string="Minimum On Hand Qty")


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    production_time =  fields.Integer('Product Production Time')

    def approved(self):
        product_template = super(ProductTemplateInherit, self).approved()
        mail_templ_id = self.env['ir.model.data'].get_object_reference(
            'custom', 'template_product_approval_mail')[1]
        template_obj = self.env['mail.template'].browse(mail_templ_id)
        send = template_obj.with_context(company=self.env.company, email=self.marketplace_seller_id.email,
                                         seller_name=self.marketplace_seller_id.name).send_mail(
            self.marketplace_seller_id.id, True)


    def reject(self):
        product_template = super(ProductTemplateInherit, self).reject()
        mail_templ_id = self.env['ir.model.data'].get_object_reference(
            'custom', 'template_product_rejection_mail')[1]
        template_obj = self.env['mail.template'].browse(mail_templ_id)
        send = template_obj.with_context(company=self.env.company, email=self.marketplace_seller_id.email,
                                         seller_name=self.marketplace_seller_id.name).send_mail(
            self.marketplace_seller_id.id, True)

    def set_pending(self):
        product_template_pending = super(ProductTemplateInherit, self).set_pending()
        mail_templ_id = self.env['ir.model.data'].get_object_reference(
            'custom', 'template_send_product_creation_mail')[1]
        template_obj = self.env['mail.template'].browse(mail_templ_id)
        send = template_obj.with_context(company=self.env.company, email=self.marketplace_seller_id.email,
                                         seller_name=self.marketplace_seller_id.name).send_mail(self.marketplace_seller_id.id, True)


    @api.depends('name', 'net_weight_per_unit','net_weight_uom')
    def _compute_complete_product_name(self):
        for record in self:
            name = ''
            if record.name:
                name += str(record.name) + ' '
            if record.net_weight_per_unit:
                name += str(int(record.net_weight_per_unit)) + ' ' + str(record.net_weight_uom)
            record.complete_name = name

    @api.depends('cust_product_category', 'energy_kg', 'sugar', 'saturated_fat', 'sodium', 'protein', 'fiber',
                 'fruit_veg')
    def _compute_nutriscore(self):
        for record in self:
            if record.cust_product_category:
                if record.cust_product_category:
                    energy_point = ''
                    sugar_point = ''
                    fat_point = ''
                    sodium_point = ''
                    protein_point = ''
                    fiber_point = ''
                    veg_point = ''
                    point_a = ''
                    point = ''
                    if record.energy_kg:
                        if record.cust_product_category == 'drink':
                            if float(record.energy_kg) <= 0:
                                energy_point = '0'
                            elif float(record.energy_kg) <= 30:
                                energy_point = '1'
                            elif float(record.energy_kg) <= 60:
                                energy_point = '2'
                            elif float(record.energy_kg) <= 90:
                                energy_point = '3'
                            elif float(record.energy_kg) <= 120:
                                energy_point = '4'
                            elif float(record.energy_kg) <= 150:
                                energy_point = '5'
                            elif float(record.energy_kg) <= 180:
                                energy_point = '6'
                            elif float(record.energy_kg) <= 210:
                                energy_point = '7'
                            elif float(record.energy_kg) <= 240:
                                energy_point = '8'
                            elif float(record.energy_kg) <= 270:
                                energy_point = '9'
                            else:
                                if float(record.energy_kg) > 270:
                                    energy_point = '10'

                        else:
                            if float(record.energy_kg) <= 335:
                                energy_point = '0'
                            elif float(record.energy_kg) <= 670:
                                energy_point = '1'
                            elif float(record.energy_kg) <= 1005:
                                energy_point = '2'
                            elif float(record.energy_kg) <= 1340:
                                energy_point = '3'
                            elif float(record.energy_kg) <= 1675:
                                energy_point = '4'
                            elif float(record.energy_kg) <= 2010:
                                energy_point = '5'
                            elif float(record.energy_kg) <= 2345:
                                energy_point = '6'
                            elif float(record.energy_kg) <= 2680:
                                energy_point = '7'
                            elif float(record.energy_kg) <= 3015:
                                energy_point = '8'
                            elif float(record.energy_kg) <= 3350:
                                energy_point = '9'
                            else:
                                if float(record.energy_kg) > 3350:
                                    energy_point = '10'
                    if record.sugar:
                        if record.cust_product_category == 'drink':
                            if float(record.sugar) <= 0:
                                sugar_point = '0'
                            elif float(record.sugar) <= 1.5:
                                sugar_point = '1'
                            elif float(record.sugar) <= 3:
                                sugar_point = '2'
                            elif float(record.sugar) <= 4.5:
                                sugar_point = '3'
                            elif float(record.sugar) <= 6:
                                sugar_point = '4'
                            elif float(record.sugar) <= 7.5:
                                sugar_point = '5'
                            elif float(record.sugar) <= 9:
                                sugar_point = '6'
                            elif float(record.sugar) <= 10.5:
                                sugar_point = '7'
                            elif float(record.sugar) <= 12:
                                sugar_point = '8'
                            elif float(record.sugar) <= 13.5:
                                sugar_point = '9'
                            else:
                                if float(record.sugar) > 13.5:
                                    sugar_point = '10'
                        else:
                            if float(record.sugar) <= 4.5:
                                sugar_point = '0'
                            elif float(record.sugar) <= 9.0:
                                sugar_point = '1'
                            elif float(record.sugar) <= 13.5:
                                sugar_point = '2'
                            elif float(record.sugar) <= 18.0:
                                sugar_point = '3'
                            elif float(record.sugar) <= 22.5:
                                sugar_point = '4'
                            elif float(record.sugar) <= 27.0:
                                sugar_point = '5'
                            elif float(record.sugar) <= 32.0:
                                sugar_point = '6'
                            elif float(record.sugar) <= 36.0:
                                sugar_point = '7'
                            elif float(record.sugar) <= 40.0:
                                sugar_point = '8'
                            elif float(record.sugar) <= 45.0:
                                sugar_point = '9'
                            else:
                                if float(record.sugar) > 45.0:
                                    sugar_point = '10'
                    if record.saturated_fat:
                        if record.cust_product_category == 'fat':
                            ags=''
                            if record.saturated_fat and record.fat:
                                ags = round((float(record.saturated_fat)/float(record.fat))*100,2)
                                if ags <= 10:
                                    fat_point = '0'
                                elif ags <= 16:
                                    fat_point = '1'
                                elif ags <= 22:
                                    fat_point = '2'
                                elif ags <= 28:
                                    fat_point = '3'
                                elif ags <= 34:
                                    fat_point = '4'
                                elif ags <= 40:
                                    fat_point = '5'
                                elif ags <= 46:
                                    fat_point = '6'
                                elif ags <= 52:
                                    fat_point = '7'
                                elif ags <= 58:
                                    fat_point = '8'
                                elif ags <= 64:
                                    fat_point = '9'
                                else:
                                    if ags > 64:
                                        fat_point = '10'

                        else:
                            if float(record.saturated_fat) <= 1:
                                fat_point = '0'
                            elif float(record.saturated_fat) <= 2:
                                fat_point = '1'
                            elif float(record.saturated_fat) <= 3:
                                fat_point = '2'
                            elif float(record.saturated_fat) <= 4:
                                fat_point = '3'
                            elif float(record.saturated_fat) <= 5:
                                fat_point = '4'
                            elif float(record.saturated_fat) <= 6:
                                fat_point = '5'
                            elif float(record.saturated_fat) <= 7:
                                fat_point = '6'
                            elif float(record.saturated_fat) <= 8:
                                fat_point = '7'
                            elif float(record.saturated_fat) <= 9:
                                fat_point = '8'
                            elif float(record.saturated_fat) <= 10:
                                fat_point = '9'
                            else:
                                if float(record.saturated_fat) > 10:
                                    fat_point = '10'
                    if record.sodium:
                        if float(record.sodium) <= 90:
                            sodium_point = '0'
                        elif float(record.sodium) <= 180:
                            sodium_point = '1'
                        elif float(record.sodium) <= 270:
                            sodium_point = '2'
                        elif float(record.sodium) <= 360:
                            sodium_point = '3'
                        elif float(record.sodium) <= 450:
                            sodium_point = '4'
                        elif float(record.sodium) <= 540:
                            sodium_point = '5'
                        elif float(record.sodium) <= 630:
                            sodium_point = '6'
                        elif float(record.sodium) <= 720:
                            sodium_point = '7'
                        elif float(record.sodium) <= 810:
                            sodium_point = '8'
                        elif float(record.sodium) <= 900:
                            sodium_point = '9'
                        else:
                            if float(record.sodium) > 900:
                                sodium_point = '10'
                    if record.protein:
                        if float(record.protein) <= 1.6:
                            protein_point = '0'
                        elif float(record.protein) <= 3.2:
                            protein_point = '1'
                        elif float(record.protein) <= 4.8:
                            protein_point = '2'
                        elif float(record.protein) <= 6.4:
                            protein_point = '3'
                        elif float(record.protein) <= 8.0:
                            protein_point = '4'
                        else:
                            if float(record.protein) > 8.0:
                                protein_point = '5'
                    if record.fiber:
                        if float(record.fiber) <= 0.9:
                            fiber_point = '0'
                        elif float(record.fiber) <= 1.9:
                            fiber_point = '1'
                        elif float(record.fiber) <= 2.8:
                            fiber_point = '2'
                        elif float(record.fiber) <= 3.7:
                            fiber_point = '3'
                        elif float(record.fiber) <= 4.7:
                            fiber_point = '4'
                        else:
                            if float(record.fiber) > 4.7:
                                fiber_point = '5'
                    if record.fruit_veg:
                        if float(record.fruit_veg) <= 40:
                            veg_point = '0'
                        elif float(record.fruit_veg) <= 60:
                            veg_point = '1'
                        elif float(record.fruit_veg) <= 80:
                            veg_point = '2'
                        elif float(record.fruit_veg) > 80:
                            veg_point = '5'
                    if record.cust_product_category == 'solid':
                        if energy_point and sugar_point and fat_point and sodium_point:
                            point_a = float(energy_point) + float(sugar_point) + float(fat_point) + float(sodium_point)
                        if point_a and protein_point and fiber_point and veg_point:
                            if 0 <= point_a < 11:
                                point = point_a - (float(protein_point) + float(fiber_point) + float(veg_point))
                            elif point_a >= 11 and float(veg_point) == 5:
                                point = point_a - (float(protein_point) + float(fiber_point) + float(veg_point))
                            else:
                                point = point_a - (float(veg_point) + float(fiber_point))
                    elif record.cust_product_category == 'cheeses':
                        if energy_point and sugar_point and fat_point and sodium_point:
                            point_a = float(energy_point) + float(sugar_point) + float(fat_point) + float(sodium_point)
                        if point_a and protein_point and fiber_point and veg_point:
                            point = point_a - (float(protein_point) + float(fiber_point) + float(veg_point))

                    elif record.cust_product_category == 'fat':
                        if energy_point and sugar_point and fat_point and sodium_point:
                            point_a = float(energy_point) + float(sugar_point) + float(fat_point) + float(sodium_point)
                        if point_a and protein_point and fiber_point and veg_point:
                            point = point_a - (float(protein_point) + float(fiber_point) + float(veg_point))

                    elif record.cust_product_category == 'drink':
                        if energy_point and sugar_point and fat_point and sodium_point:
                            point_a = float(energy_point) + float(sugar_point) + float(fat_point) + float(sodium_point)
                        if point_a and protein_point and fiber_point and veg_point:
                            if 0 <= point_a < 11:
                                point = point_a - (float(protein_point) + float(fiber_point) + float(veg_point))
                            elif point_a >= 11 and float(veg_point) == 5:
                                point = point_a - (float(protein_point) + float(fiber_point) + float(veg_point))
                            else:
                                point = point_a - (float(veg_point) + float(fiber_point))
                    if point and record.cust_product_category != 'drink':
                        if point < 0:
                            record.nutriscore = 'Nutriscore A'
                        elif point < 3:
                            record.nutriscore = 'Nutriscore B'
                        elif point < 11:
                            record.nutriscore = 'Nutriscore C'
                        elif point < 19:
                            record.nutriscore = 'Nutriscore D'
                        elif point >= 19:
                            record.nutriscore = 'Nutriscore E'
                        else:
                            record.nutriscore = ' '
                    elif point and record.cust_product_category == 'drink':
                        if record.natural_water == 'yes':
                            record.nutriscore = 'Nutriscore A'
                        elif point < 2:
                            record.nutriscore = 'Nutriscore B'
                        elif point < 6:
                            record.nutriscore = 'Nutriscore C'
                        elif point < 10:
                            record.nutriscore = 'Nutriscore D'
                        elif point >= 10:
                            record.nutriscore = 'Nutriscore E'
                        else:
                            record.nutriscore = ' '
                    else:
                        record.nutriscore = ' '
            else:
                record.nutriscore = ' '








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
    nutriscore = fields.Char("Nutriscore", compute="_compute_nutriscore", store=True)
    energy_kg = fields.Char("Energy (kj)")
    cal_energy_kg = fields.Float("Calculate Energy (kj)")
    energy_kcal = fields.Char("Energy (kcal)")
    cal_energy_kcal = fields.Float("Calculate Energy (kcal)")
    fat = fields.Char("Total Fats")
    cal_fat = fields.Float("Fats")
    saturated_fat = fields.Char("Total saturated fats")
    cal_saturated_fat = fields.Float("Calculate Totally saturated fats")
    mono_unsaturated_fats = fields.Char("Monounsaturated Fats")
    cal_mono_unsaturated_fats = fields.Float("Calculate Monounsaturated Fats")
    poly_unsaturated_fats = fields.Char("Polyunsaturated fats")
    cal_poly_unsaturated_fats = fields.Float("Calculate Polyunsaturated fats")
    carbohydrates = fields.Char("Carbohydrates")
    cal_carbohydrates = fields.Float("Calculate Carbohydrates")
    sugar = fields.Char("Sugars")
    cal_sugar = fields.Float("Calculate Sugars")
    protein = fields.Char("Proteins")
    cal_protein = fields.Float("Calculate Proteins")
    salt = fields.Char("Salt")
    cal_salt = fields.Float("Calculate Salt")
    sodium = fields.Char("Sodium")
    cal_sodium = fields.Float("Calculate Sodium")
    fruit_veg = fields.Char("Fruits,vegetables,legumes,nuts,canola,nut & olive oils")
    cal_fruit_veg = fields.Float("Calculate FVLNRNOO")
    fiber = fields.Char("Dietary Fiber")
    cal_fiber = fields.Float("Calculate Dietary Fiber")
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
    net_content_uom = fields.Selection([('gram', 'gram'),('ml', 'ml')],string="UOM", default='gram')
    drained_weight_per_unit = fields.Float("Drained content per single unit")
    drained_weight_uom = fields.Selection([('gram', 'gram'), ('ml', 'ml')], string="UOM", default='gram')
    net_weight_per_unit = fields.Float("Net weight per single unit")
    net_weight_uom = fields.Selection([('gram', 'gram'), ('ml', 'ml')], string="UOM", default='gram')
    gross_weight_per_unit = fields.Float("Gross weight per single unit")
    gross_weight_uom = fields.Selection([('gram', 'gram'), ('ml', 'ml')], string="UOM", default='gram')
    net_content_per_carton = fields.Float("Net content carton")
    net_carton_uom = fields.Selection([('gram', 'gram'), ('ml', 'ml')], string="UOM", default='gram')
    drained_weight_per_carton = fields.Float("Drained content carton")
    drained_carton_uom = fields.Selection([('gram', 'gram'), ('ml', 'ml')], string="UOM", default='gram')
    net_weight_per_carton = fields.Float("Net weight carton")
    net_weight_carton_uom = fields.Selection([('gram', 'gram'), ('ml', 'ml')], string="UOM", default='gram')
    gross_weight_per_carton = fields.Float("Gross weight carton")
    gross_weight_carton_uom = fields.Selection([('gram', 'gram'), ('ml', 'ml')], string="UOM", default='gram')
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
    max_cases_weight_transport = fields.Float("Max cases on weight per transport")
    cost_sending_per_case = fields.Float("Cost sending per case")
    max_cases_by_weight_volume = fields.Float("Max cases by weight and volume")
    cost_sending_per_full_box = fields.Float("Cost sending per full box")
    used_box_volume = fields.Float("Used box volume")
    cost_full_box = fields.Float("Cost full box")
    percentage_cost_case = fields.Float("Percentage cost on case")
    reserve_full_box = fields.Float("Reserve full box")
    cost_effective_x_purchase = fields.Float("Cost effective from x purchase")
    margin_per_box = fields.Float("Margin per box")
    box_length = fields.Float("Length Kairos box")
    box_width = fields.Float("Width Kairos box")
    box_height = fields.Float("Height Kairos box")
    box_maximum_weight = fields.Float("Maximum weight Kairos box")
    complete_name = fields.Char(string="Complete Name", compute="_compute_complete_product_name", store=True)
    cust_product_category = fields.Selection(
        [('solid', 'Solid – liquid foods'), ('cheeses', 'Cheeses'), ('fat', 'Added fats'), ('drink', 'Drinks')],
        string="Product Type")
    natural_water = fields.Selection(
        [('yes', 'YES'), ('no', 'NO')],
        string="Natural Water")
    retail_sales = fields.Selection(
        [('yes', 'YES'), ('planning', 'Planning'), ('never', 'Never')],
        string="Sales in retail")
    plan_retail_sales = fields.Char("Where would you sell in retail?")
    internal_ref_su = fields.Char("Internal Reference Single Unit")
    internal_ref_c = fields.Char("Internal Reference Carton")
    exclusively_id = fields.Many2many('partner.speciality', string='Exclusively')
    packaging = fields.Selection([('brik', 'Brik'),('Can', 'can'),('glass', 'Glass'),
         ('large', 'Large'), ('mill', 'Mill'),('pet', 'Pet'),('portion', 'Portion'),
         ('pouch', 'Pouch'), ('small', 'Small'), ('packaging', 'Packaging'),
         ('tetra', 'Tetra'), ('vending', 'Vending')],'Packaging')
    nutritional_structure = fields.Selection([('brik', 'Dehydrated'),('liquid', 'Liquid'),('oil', 'Oil'),
         ('pasta', 'Pasta'), ('powder', 'Powder'), ('tablets', 'Tablets')], 'Nutritional structure')
    product_quantity_type = fields.Selection([('article', 'Sell per article'), ('case', 'Sell per case'), ('article_case', 'Sell per article and case')],
                                            'Product Quantity Type')
    first_warning_min_carton = fields.Integer("First warning minimum stock in cartons")
    min_stock_carton = fields.Integer("Minimum stock in cartons")
    single_unit_package = fields.Char("Single unit packaging")
    cost_type = fields.Selection([('unit', 'Single unit cost'),('carton', 'Carton cost')],'Type')


    def name_get(self):
        result = []
        name = ''
        for res in self:
            if res.name:
                name += str(res.name) + ' '
            if res.net_weight_per_unit:
                name += str(int(res.net_weight_per_unit)) + ' ' + str(res.net_weight_uom)
            result.append((res.id, name))
        return result

    @api.onchange('volume_unit','box_length','box_width','box_height','box_maximum_weight')
    def _onchange_get_fulfilment_cost(self):
        for record in self:
            if record.volume_unit and record.box_length and record.box_width and record.box_height and record.box_maximum_weight:
                cases=[]
                v1_t1 =int(record.box_length/record.length_unit)*int(record.box_width/record.width_unit)*int(record.box_height/record.height_unit)
                cases.append(v1_t1)
                v1_t2 =int(record.box_width/record.length_unit)*int(record.box_height/record.width_unit)*int(record.box_length/record.height_unit)
                cases.append(v1_t2)
                v1_t3 =int(record.box_height/record.length_unit)*int(record.box_length/record.width_unit)*int(record.box_width/record.height_unit)
                cases.append(v1_t3)
                v2_t1 =int(record.box_length/record.length_unit)*int(record.box_height/record.width_unit)*int(record.box_width/record.height_unit)
                cases.append(v2_t1)
                v2_t2 =int(record.box_width/record.length_unit)*int(record.box_length/record.width_unit)*int(record.box_height/record.height_unit)
                cases.append(v2_t2)
                v2_t3 =int(record.box_height/record.length_unit)*int(record.box_width/record.width_unit)*int(record.box_length/record.height_unit)
                cases.append(v2_t3)
                max_weight_kg = int(record.box_maximum_weight /1.08)
                adjust_weight_kg = int(int(record.box_maximum_weight * (80/100))/1.08)
                max_case_volume = min(max(cases), 9)
                max_case_weight =min(max_weight_kg,adjust_weight_kg)
                cost_pending_pr_case = round((1.85+(0.3*min(max_case_volume,max_case_weight))+1.23+5.3)/min(max_case_volume,max_case_weight),3)





    @api.onchange('energy_kg')
    def _onchange_get_cal_energy_kg(self):
        for record in self:
            if record.energy_kg:
                record.cal_energy_kg = float(record.energy_kg)/8400*100

    @api.onchange('energy_kcal')
    def _onchange_get_cal_energy_kcal(self):
        for record in self:
            if record.energy_kcal:
                record.cal_energy_kcal = float(record.energy_kcal) / 2000 * 100
                record.energy_kg = str(round(float(record.energy_kcal) * 4.184))


    @api.onchange('fat')
    def _onchange_get_cal_fat(self):
        for record in self:
            if record.fat:
                record.cal_fat = float(record.fat) / 70 * 100


    @api.onchange('saturated_fat')
    def _onchange_get_cal_saturated_fat(self):
        for record in self:
            if record.saturated_fat:
                record.cal_saturated_fat = float(record.saturated_fat) / 20 * 100

    @api.onchange('carbohydrates')
    def _onchange_get_cal_carbohydrates(self):
        for record in self:
            if record.carbohydrates:
                record.cal_carbohydrates = float(record.carbohydrates) / 260 * 100

    @api.onchange('sugar')
    def _onchange_get_cal_sugar(self):
        for record in self:
            if record.sugar:
                record.cal_sugar = float(record.sugar) / 90 * 100

    @api.onchange('protein')
    def _onchange_get_cal_protein(self):
        for record in self:
            if record.protein:
                record.cal_protein = float(record.protein) / 50 * 100

    @api.onchange('salt')
    def _onchange_get_cal_salt(self):
        for record in self:
            if record.salt:
                record.cal_salt = float(record.salt) / 6 * 100
                record.sodium = str(round(float(record.salt) / 2.5 * 1000))

    # @api.onchange('sodium')
    # def _onchange_get_cal_sodium(self):
    #     for record in self:
    #         if record.sodium:
    #             record.cal_sodium = record.sodium / 2.5 * 1000

    @api.onchange('length_unit', 'width_unit', 'height_unit')
    def _onchange_get_volume_unit(self):
        for record in self:
            record.volume_unit = record.length_unit * record.width_unit * record.height_unit

    @api.onchange('length_carton', 'width_carton', 'height_carton')
    def _onchange_get_volume_carton(self):
        for record in self:
            record.volume_carton = record.length_carton * record.width_carton * record.height_carton





    # product_place = fields.Char("Place of origin organic product")
    # origin_type = fields.Char("Type of origin")
    # method_capture = fields.Many2one("method.capture", "Method of capture")
    # area_capture = fields.Many2one("area.capture", "Area of capture")
    #
    # nutritional_info = fields.Text("Nutritional information")
    # allergens = fields.Char("Allergens")
    # pallet_length = fields.Char("Pallet Length")
    # pallet_height = fields.Char("Pallet height")





    # file_upload = fields.One2many(comodel_name='ir.attachment',inverse_name='product_id', string="Certificates of the product")
    # attachment_ids = fields.Many2many(comodel_name='ir.attachment', string='Attachments')
    certificate_ids = fields.One2many('company.certificate.tree', 'product_id', 'Certificates')

    @api.model
    def create(self, vals):
        res = super(ProductTemplateInherit, self).create(vals)
        if res:
            res.write({'default_code': self.env['ir.sequence'].next_by_code('internal.ref') or '',
                       'internal_ref_su': self.env['ir.sequence'].next_by_code('internal.ref.su') or '',
                       'internal_ref_c': self.env['ir.sequence'].next_by_code('internal.ref.c') or '',
                       })
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
