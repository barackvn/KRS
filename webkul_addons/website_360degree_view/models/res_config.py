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

from odoo import api, fields, models, _
from odoo.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)


class Website360ViewConfig(models.TransientModel):
    _name = 'website.360.view.config'
    _inherit = 'res.config.settings'

    
    enable_360_view = fields.Boolean(
        string="Enable 360° view", help = "Enable 360° view of product on you website.",related = 'website_id.enable_360_view',readonly = False)

    @api.depends('enable_360_view')
    def on_change_enable_360_view(self):
        product_temp_objs = self.env['product.template'].search([])
        if self.enable_360_view:
            for obj in product_temp_objs:
                obj.write({"product_360_view": True,
                           "product_default_view": False})
        else:
            for obj in product_temp_objs:
                obj.write({"product_default_view": True,
                           "product_360_view": False})
