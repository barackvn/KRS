# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import models, fields, api
from odoo.tools.translate import html_translate

class InventiveMegaMenus(models.Model):
    _inherit="website.menu"
    # # which redirect to website in editor mode
    # def action_mega_menu_edit_mode(self, context=None):
    #     url = '/shop?model=website.menu&enable_editor=1'
    #     return {
    #         'name': ('Inventive Mega Menu Editing Mode'),
    #         'type': 'ir.actions.act_url',
    #         'url': url,
    #         'target': 'new',
    #     }
    #
    # is_inventive_mega_menu      = fields.Boolean("Is Mega Menu", default=False)
    # menu_html_content           = fields.Html('Menu Design html',translate=html_translate,readoly=True)
    show_on_hover               = fields.Boolean(string="Show On Hover")
    mega_menu_icon              = fields.Binary("Menu Icon")
