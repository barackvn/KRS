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
from odoo.tools.translate import html_translate

class SellerProfileTabs(models.Model):
    _name = 'seller.profile.tabs'
    _order = "sequence, profile_tab_id"
    _rec_name = "profile_tab_id"
    _description = "Seller Profile Tabs"

    website_published = fields.Boolean("Published")
    sequence = fields.Integer("Sequence" )
    profile_tab_id = fields.Many2one("profile.tab", "Tab", required=1)
    content = fields.Html("Content", required=1, sanitize_attributes=False, translate=html_translate)
    marketplace_seller_id  = fields.Many2one(comodel_name='res.partner', string='Seller')
    active = fields.Boolean("Active", related= "profile_tab_id.active")

    def toggle_website_published(self):
        """ Inverse the value of the field ``website_published`` on the records in ``self``. """
        for record in self:
            record.website_published = not record.website_published

class ProfileTab(models.Model):
    _name = "profile.tab"
    _description = "Model for Profile Tabs"

    name = fields.Char("Name", required=True)
    active = fields.Boolean("Active", default=1)
