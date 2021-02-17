import re
import base64
import datetime

from odoo import fields, models, api, _, tools
from odoo.addons.iap import jsonrpc
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
import logging

_logger = logging.getLogger(__name__)


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

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
