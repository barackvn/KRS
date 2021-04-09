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
from odoo.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)

class MarketplaceConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    comm_type = fields.Selection([
        ('product','Product'),
        ('category','Category'),
        ('seller','Seller')],
        string= 'Commission Type',
        default = 'product',
        required = True,
    )
    category_comm = fields.Selection([('minimum','Minimum'),('maximum','Maximum')], string="Category Commission", default="minimum")
    mp_comm_method = fields.Selection([
        ('percent','Percent(%)'),
        ('fix','Fixed'),
        ('percent_and_fix','% + Fixed'),
        ('fix_and_percent','Fixed + %')],
        string=" Commission Method",
        default='fix',
        required=True,
    )
    mp_fix_commission = fields.Float(string= 'Fix Commission')

    def set_values(self):
        res = super(MarketplaceConfigSettings, self).set_values()
        self.env['ir.default'].sudo().set('res.config.settings', 'comm_type', self.comm_type)
        self.env['ir.default'].sudo().set('res.config.settings', 'category_comm', self.category_comm)
        self.env['ir.default'].sudo().set('res.config.settings', 'mp_comm_method', self.mp_comm_method)
        self.env['ir.default'].sudo().set('res.config.settings', 'mp_fix_commission', self.mp_fix_commission)
        return True

    def get_values(self, fields=None):
        res = super(MarketplaceConfigSettings, self).get_values()
        comm_type = self.env['ir.default'].sudo().get('res.config.settings', 'comm_type')
        category_comm = self.env['ir.default'].sudo().get('res.config.settings', 'category_comm')
        mp_comm_method = self.env['ir.default'].sudo().get('res.config.settings', 'mp_comm_method')
        mp_fix_commission = self.env['ir.default'].sudo().get('res.config.settings', 'mp_fix_commission')
        res.update(
            {
                'comm_type'     :   comm_type,
                'category_comm' :   category_comm,
                'mp_comm_method'   :   mp_comm_method,
                'mp_fix_commission'    :   mp_fix_commission,
            }
        )
        return res

    def execute(self):
        res = super(MarketplaceConfigSettings, self).execute()
        for rec in self:
            if rec.mp_fix_commission < 0:
                raise Warning(_("Fix Commission should be greater than 0."))
        return res
