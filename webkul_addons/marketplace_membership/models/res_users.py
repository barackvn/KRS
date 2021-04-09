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
from odoo.tools.translate import _
from ast import literal_eval
# from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT, ustr
# from odoo import SUPERUSER_ID
# from odoo.addons.auth_signup.models.res_users import SignupError


import logging
_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    def copy(self, default=None):
        self.ensure_one()
        user_obj = super(ResUsers, self).copy(default=default)
        if self._context and self._context.get('is_seller'):
            # Set Default fields for seller (i.e: payment_methods, commission,
            # location_id, etc...)
            no_of_product = self.env['res.config.settings'].get_mp_global_field_value('mp_no_of_product')
            user_obj.partner_id.write({
                # 'free_membership': True,
                'no_of_product' : no_of_product,
            })
        return user_obj
