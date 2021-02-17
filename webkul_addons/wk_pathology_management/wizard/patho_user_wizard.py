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

from odoo import models,fields,api
from odoo import tools
import logging
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)

class PathoUserWizard(models.TransientModel):
    _name= "patho.user.wizard"
    _description = "Pathology User Wizard"

    message = fields.Char("Message")
    user_id = fields.Many2one("res.users", "User")

    
    def action_view_current_user(self):
        for rec in self:
            action = self.env.ref('base.action_res_users').read()[0]
            action['views'] = [(self.env.ref('base.view_users_form').id, 'form')]
            action['res_id'] = rec.user_id.id
            return action
