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


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    pre_advice = fields.Boolean("Pre Advice")
    amount_of_pallets = fields.Float("Amount of pallets")
    # measure_pallets = fields.Char(string="Measurements pallet", placeholder="Brut weight and LxWxH")
    amount_of_case_pallets = fields.Float("Amount of cases per pallet")
    measure_height = fields.Char("Height")
    measure_length = fields.Char("Length")
    pre_advice_type = fields.Selection([('transfer', 'Transfer'), ('return', 'Return')], String="Pre Advice Type",
                                       default="transfer")
    depart_date = fields.Date("Depart Date")
    arrival_date = fields.Date("Arrival Date")

    @api.onchange('partner_id','picking_type_id','location_id')
    def _onchange_get_seller_location(self):
        for record in self:
            if record.pre_advice and record.partner_id and record.picking_type_id:
                if record.picking_type_id.default_location_src_id == record.location_id:
                    record.location_id = record.partner_id.seller_location_id.id


    @api.onchange('pre_advice_type')
    def _onchange_get_location_swipe(self):
        for record in self:
            if record.location_id and record.location_dest_id:
                source = record.location_dest_id
                dest = record.location_id
                record.location_id = source
                record.location_dest_id = dest

class StockLocationInherit(models.Model):
    _inherit = 'stock.location'

    seller_id = fields.Many2one("res.partner", string="Seller")
