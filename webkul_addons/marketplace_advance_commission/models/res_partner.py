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


from odoo import models, fields, api, _
from odoo.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)

manager_fields = []

class ResPartner(models.Model):
    _inherit = 'res.partner'

    comm_method = fields.Selection([
        ('percent','Percent(%)'),
        ('fix','Fixed'),
        ('percent_and_fix','% + Fixed'),
        ('fix_and_percent','Fixed + %')],
        string="Commission Method",
        default = lambda self: self.env['ir.default'].get('res.config.settings', 'mp_comm_method'),
        read=['odoo_marketplace.marketplace_draft_seller_group'], write=['odoo_marketplace.marketplace_manager_group'],
        copy=False, track_visibility='onchange',
        )
    fix_commission = fields.Float(string= 'Fixed Commission',
        default = lambda self: self.env['ir.default'].get('res.config.settings', 'mp_fix_commission'),
        read=['odoo_marketplace.marketplace_draft_seller_group'], write=['odoo_marketplace.marketplace_manager_group'],
        copy=False,
        track_visibility='onchange',
    )
    manager_fields.extend(['comm_method','fix_commission','commission','seller_payment_limit','next_payment_request','auto_product_approve',
        'auto_approve_qty','location_id','warehouse_id','allow_product_variants',
        'total_mp_payment','paid_mp_payment','balance_mp_payment', 'state'])

    @api.onchange('fix_commission')
    def check_fix_commission(self):
        if self.fix_commission < 0.0:
            raise Warning(_('Fix Commission should be greater than zero.'))

    @api.onchange("set_seller_wise_settings")
    def on_change_seller_wise_settings(self):
        res = super(ResPartner, self).on_change_seller_wise_settings()
        if self.set_seller_wise_settings:
            vals = {
                "comm_method": self.env['ir.default'].get(
                    'res.config.settings', 'mp_comm_method'
                )
            }
            vals["fix_commission"] = self.env['ir.default'].get(
                'res.config.settings', 'mp_fix_commission')
            self.update(vals)

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        for _ in self:
            if vals.get("fix_commission") and vals.get("fix_commission", "") < 0.0:
                raise Warning(_("Fix Commission should be greater than 0."))
        return res

    @api.onchange("seller")
    def on_change_seller(self):
        res = super(ResPartner, self).on_change_seller()
        resConfig = self.env['res.config.settings']
        self.comm_method = resConfig.get_mp_global_field_value("mp_comm_method")
        self.fix_commission = resConfig.get_mp_global_field_value("mp_fix_commission")
        return res
