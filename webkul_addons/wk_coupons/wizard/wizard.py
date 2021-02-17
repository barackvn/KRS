#  -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################

from odoo import api, fields, models, _

class WizardMessage(models.TransientModel):
	_name = "wizard.message"
	_description = "Wizard Message"
	text = fields.Text('Message')
