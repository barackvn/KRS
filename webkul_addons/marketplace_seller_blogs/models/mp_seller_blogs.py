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

from odoo import models,fields,api,_
import json
from odoo.addons.website.controllers.main import QueryURL
from lxml import etree
import logging
logger = logging.getLogger(__name__)

class BlogPost(models.Model):
    _inherit = "blog.post"

    @api.model
    def _set_seller_id(self):
        if self._context.get('mp_seller_blog'):
            user_obj = self.env['res.users'].sudo().browse(self._uid)
            if user_obj.partner_id and user_obj.partner_id.seller:
                return user_obj.partner_id.id
            return self.env['res.partner']

    marketplace_seller_id = fields.Many2one("res.partner", string="Seller", default=_set_seller_id, copy=False)
    seller_blog_content = fields.Html(string="Blog Content", copy=False, translate=True)
    state = fields.Selection([('draft', 'Draft'), ('pending', 'Pending'), (
        'approved', 'Approved'), ('rejected', 'Rejected')], "Marketplace Blog Status", default='draft', copy=False, track_visibility='onchange')

    # update enhancement with banner for frontend
    cover_images = fields.Binary("Cover images")

    def set_cover_background(self, reset=None):
        for rec in self:
            cover_properties = json.loads(rec.cover_properties)
            if reset:
                cover_properties['background-image'] = "none"
            else:
                cover_properties[
                    'background-image'
                ] = f"url(/web/image/blog.post/{str(rec.id)}/cover_images)"
                cover_properties['resize_class'] = "cover"
            rec.cover_properties = json.dumps(cover_properties)

    @api.model
    def create(self, vals):
        res = super(BlogPost, self).create(vals)
        if vals.get('cover_images', False):
            res.set_cover_background()
        return res

    def write(self, vals):
        if vals.get('cover_images') != None:
            if vals.get('cover_images'):
                self.set_cover_background()
            else:
                self.set_cover_background(reset=True)
        return super(BlogPost, self).write(vals)


    def button_approve_blog(self):
        for rec in self:
            rec.state = "approved"

    def button_reject_blog(self):
        for rec in self:
            rec.state = "rejected"
            rec.is_published = False

    def button_set_pending_blog(self):
        for rec in self:
            rec.blog_auto_approve()

    def button_set_draft_blog(self):
        for rec in self:
            rec.state = "draft"

    def blog_auto_approve(self):
        for obj in self:
            if obj.marketplace_seller_id.auto_blog_approve:
                obj.write({"state": "pending"})
                obj.sudo().button_approve_blog()
            else:
                obj.write({"state": "pending"})
        return True

    def toggle_is_published(self):
        for record in self:
            record.sudo().is_published = not record.sudo().is_published

    def find_url(self, blog_id, tag_id):
        blog_url = QueryURL('', ['blog', 'tag'])
        return blog_url(blog= blog_id, tag= tag_id, date_begin=False, date_end=False)

class Blog(models.Model):
    _inherit = 'blog.blog'

class BlogTag(models.Model):
    _inherit = 'blog.tag'

    allow_to_seller = fields.Boolean(string="Allow to Seller", default= False)
    post_ids = fields.Many2many('blog.post', string='Posts',
        domain = lambda self: [('marketplace_seller_id','in',self.env['blog.tag'].compute_login_userid()),('state','=','approved')] if self._context.get('mp_blog_tag') else [],)

    def compute_login_userid(self):
        seller_group = self.env['ir.model.data'].get_object_reference(
            'odoo_marketplace', 'marketplace_seller_group')[1]
        officer_group = self.env['ir.model.data'].get_object_reference(
            'odoo_marketplace', 'marketplace_officer_group')[1]
        groups_ids = self.env.user.sudo().groups_id.ids
        if seller_group in groups_ids:
            login_ids = []
            if officer_group not in groups_ids:
                login_ids.append(self.env.user.sudo().partner_id.id)
            else:
                obj = self.env['res.partner'].search([('seller','=',True)])
                login_ids.extend(rec.id for rec in obj)
            return login_ids

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(BlogTag, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        obj = self.env['blog.tag'].browse(self._context.get('active_ids'))
        doc = etree.XML(res['arch'])
        login_ids = obj.compute_login_userid()
        if self._context.get('mp_blog_tag'):
            for node in doc.xpath("//field[@name='post_ids']"):
                node.set(
                    'domain',
                    f"[('marketplace_seller_id','in',{login_ids}),('state','=','approved')]",
                )
        res['arch'] = etree.tostring(doc)
        return res
