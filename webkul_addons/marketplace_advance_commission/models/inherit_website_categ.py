# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import models,fields,api,_
import logging
_logger = logging.getLogger(__name__)

class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    comm_method = fields.Selection([
        ('percent','Percent(%)'),
        ('fix','Fixed'),
        ('percent_and_fix','% + Fixed'),
        ('fix_and_percent','Fixed + %')],
        string="Commission Method",
        read=['odoo_marketplace.marketplace_seller_group'],write=['odoo_marketplace.marketplace_officer_group'],
        copy=False,
    )
    percent_commission = fields.Float(string= 'Percent Commission',
        read=['odoo_marketplace.marketplace_seller_group'],write=['odoo_marketplace.marketplace_officer_group'],
        copy=False
    )
    fix_commission = fields.Float(string= 'Fixed Commission',
        read=['odoo_marketplace.marketplace_seller_group'],write=['odoo_marketplace.marketplace_officer_group'],
        copy=False
    )
    mp_config_currency_id = fields.Many2one('res.currency', string='Currency',compute = 'compute_mp_config_currency_id')

    def compute_mp_config_currency_id(self):
        for obj in self:
            obj.mp_config_currency_id = self.env['ir.default'].get('res.config.settings', 'mp_currency_id') or self.env.user.company_id.currency_id
