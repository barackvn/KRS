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

import json
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class res_users(models.Model):
    _inherit = 'res.users'

    def _auth_oauth_signin(self, provider, validation, params):
        context = dict(self._context or {})
        state = json.loads(params['state'])
        context["is_seller"] = state.get('s',False)
        test = super(res_users, self.with_context(context))._auth_oauth_signin(provider, validation, params)
        return test
