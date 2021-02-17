# -*- coding: utf-8 -*-
#################################################################################
##    Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################
from odoo import api, fields, models, _
from odoo.exceptions import Warning


class WkWizardMessage(models.TransientModel):
    _name = "wk.wizard.message"

    text = fields.Text(string='Message')
