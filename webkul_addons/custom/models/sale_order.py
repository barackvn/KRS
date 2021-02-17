import re
import base64
import datetime

from odoo import fields, models, api, _, tools
from odoo.addons.iap import jsonrpc
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
import logging

_logger = logging.getLogger(__name__)



class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'


    