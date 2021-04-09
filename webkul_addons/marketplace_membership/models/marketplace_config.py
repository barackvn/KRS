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
from odoo.tools.translate import _

from odoo.exceptions import except_orm, Warning, RedirectWarning

import logging
_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    mp_no_of_product = fields.Integer(string="# of Products")
    mp_membership_plan_link_label = fields.Text(
        string="Seller Membership Plan Link Label", related="website_id.mp_membership_plan_link_label", readonly=False)


    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.default'].sudo().set(
            'res.config.settings', 'mp_no_of_product', self.mp_no_of_product)
        return True


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        mp_no_of_product = self.env['ir.default'].get(
            'res.config.settings', 'mp_no_of_product')
        res.update({"mp_no_of_product" : mp_no_of_product})
        return res


    def execute(self):
        for rec in self:
            if rec.mp_no_of_product < 0 :
                raise Warning(_("Amount Limit can't be negative."))
        return super(ResConfigSettings, self).execute()
