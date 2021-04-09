# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import models, fields, api, _
from odoo import tools, api

from odoo.tools.translate import _


class website(models.Model):
    _inherit = 'website'

    enable_360_view = fields.Boolean(
        string="Enable 360° view", help="Enable 360° view of product on you website.")
