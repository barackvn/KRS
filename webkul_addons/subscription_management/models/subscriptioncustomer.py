# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
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
##########################################################################



from odoo import api, fields, models
from odoo.exceptions import UserError
import logging

_log=logging.getLogger(__name__)

class subscriptioncustomer(models.Model):
    _inherit='res.partner'

    all_subscription = fields.One2many('subscription.subscription',inverse_name='customer_name')

