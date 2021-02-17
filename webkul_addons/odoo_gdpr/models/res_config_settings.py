# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # @api.multi
    def open_odoo_gdpr_conf(self):
        odoo_gdpr = self.env["odoo.gdpr"].sudo().search([],limit=1)
        return {
        'type': 'ir.actions.act_window',
        'name': 'Odoo Gdpr Configuration',
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'odoo.gdpr',
        'res_id': odoo_gdpr.id,
        'target': 'current',
        }
