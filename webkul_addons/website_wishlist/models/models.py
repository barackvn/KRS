# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import api, fields, models, tools, _
# import logging
# _logger = logging.getLogger(__name__)

class Users(models.Model):
    _inherit = 'res.users'

    # @api.multi
    def add_product(self, product_id):
        User = self.env.user
        if User.partner_id:
            vals = {
                'product_id': product_id,
                'partner_id':User.partner_id.id,
                'user_id': User.id,
            }
            self.env['website.wishlist'].create(vals)
            if User.partner_id.website_wishlist:
                return len(User.partner_id.website_wishlist)
        return False

    # @api.multi
    def remove_product(self, product_id):
        User = self.env.user
        if User.partner_id:
            wishlist_line_obj = self.env['website.wishlist'].search([('product_id','=',product_id),('partner_id','=',User.partner_id.id)])
            if wishlist_line_obj:
                wishlist_line_obj.sudo().unlink()
                return len(User.partner_id.website_wishlist) or 0
        return False


class Website(models.Model):
    _inherit = 'website'

    # @api.multi
    def get_wishlist_products(self):
        User = self.env.user
        if User.partner_id.website_wishlist:
            return User.partner_id.website_wishlist
        return []

    # @api.multi
    def check_wishlist_product(self):
        User, product_ids = self.env.user, []
        if User.partner_id.website_wishlist:
            for wishlist_line in User.partner_id.website_wishlist:
                product_ids.append(wishlist_line.product_id.id)
            if product_ids:
                return product_ids
        return []

class Partner(models.Model):
    _inherit = 'res.partner'

    website_wishlist = fields.One2many('website.wishlist','partner_id', string='Wishlist')



class WebsiteWishlist(models.Model):
    _name = "website.wishlist" 


    @api.model
    def create(self, vals):
        if  'product_id' in vals and  'partner_id' in vals:
            check = self.search([('product_id','=',vals['product_id']),('partner_id','=',vals['partner_id'])])
            if check:
                return check[0]
        return super(WebsiteWishlist, self).create(vals)

    # @api.multi
    def get_wishlist_products(self):
        User = self.env.user
        if User.partner_id.website_wishlist:
            return User.partner_id.website_wishlist
        return False

    product_id = fields.Many2one('product.product',string='Product')
    partner_id = fields.Many2one('res.partner', string='Partner')
    user_id = fields.Integer(string='User ID')
