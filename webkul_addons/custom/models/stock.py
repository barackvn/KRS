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
    measure_pallets = fields.Char(string="Measurements pallet", placeholder="Brut weight and LxWxH")
    amount_of_case_pallets = fields.Float("Amount of cases per pallet")
