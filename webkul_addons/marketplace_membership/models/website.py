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

from odoo import api, models, fields, tools, _
import logging
_logger = logging.getLogger(__name__)



class Website(models.Model):
    _inherit = 'website'

    mp_membership_plan_link_label = fields.Text(string="Seller Membership Plan Link Label", translate=True, default="Seller Membership Plans")

    @api.model
    def cart_line_check_membership(self, product_id=None, order_id=None):
        if order_id and product_id:
            order_obj = self.env["sale.order"].browse(order_id)
            for line in order_obj.order_line:
                if line.product_id.wk_mp_membership and line.product_id.id != product_id:
                    return True
        return False
