# -*- coding: utf-8 -*-
##########################################################################
# 2010-2017 Webkul.
#
# NOTICE OF LICENSE
#
# All right is reserved,
# Please go through this link for complete license : https://store.webkul.com/license.html
#
# DISCLAIMER
#
# Do not edit or add to this file if you wish to upgrade this module to newer
# versions in the future. If you wish to customize this module for your
# needs please refer to https://store.webkul.com/customisation-guidelines/ for more information.
#
# @Author        : Webkul Software Pvt. Ltd. (<support@webkul.com>)
# @Copyright (c) : 2010-2017 Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# @License       : https://store.webkul.com/license.html
#
##########################################################################

from odoo import models, fields, api, _
from odoo.tools.translate import html_translate

import logging
_logger = logging.getLogger(__name__)

class SellerStory(models.Model):
    _name = 'seller.story'
    _description = "Seller Story."
    _inherit = ['website.published.mixin']

    name = fields.Char(string="Story Title", required=True, default=lambda self: self.seller_id.name + "Story" if self.seller_id else False)
    image = fields.Binary(string="Thumbnail Image", default=lambda self: self.seller_id.image_1920 if self.seller_id else False)
    short_description = fields.Text(string="Short Description", translate=True)
    story_video_link = fields.Char(string="Youtube Video ID")
    description = fields.Html(string="Complete Description", sanitize_attributes=False, translate=html_translate)
    seller_id = fields.Many2one("res.partner", domain=[("seller", "=", True)], inverse='_link_story_to_seller', required=True, default=lambda self: self.env.user.partner_id.id if self.env.user.partner_id and self.env.user.partner_id.seller else self.env['res.partner'])
    designation = fields.Char("Designation")
    is_popular = fields.Boolean("Popular Story")

    _sql_constraints = [('seller_id_uniqe', 'unique(seller_id)', _('Seller story for this seller has been already created.'))]

    def _link_story_to_seller(self):
        for rec in self:
            if rec.seller_id:
                self.seller_id.seller_story_id = self.id

    @api.onchange("seller_id")
    def onchange_seller_id(self):
        if self.seller_id:
            self.image = self.seller_id.image_1920

    def toggle_website_published(self):
        """ Inverse the value of the field ``website_published`` on the records in ``self``. """
        for record in self:
            record.website_published = not record.website_published

    def toggle_popular_story(self):
        """ Inverse the value of the field ``is_popular`` on the records in ``self``. """
        for record in self:
            record.is_popular = not record.is_popular
