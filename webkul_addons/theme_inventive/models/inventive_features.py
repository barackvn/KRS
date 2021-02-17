# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import models, fields,api
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class InventiveFeatureWarning(models.TransientModel):
    _name = 'wizard.feature.message'
    _description = 'Wizard that show warning if user try to publish redazzled feature'
    msg = fields.Char(string='message', readonly=True)

    def publish_on_website(self):
        active_record = self.env[self._context['active_model']].browse([self._context['active_id']])
        feature = self.env[self._context['active_model']].browse([self._context['feature_id']])
        self.published_feature_name=active_record.name
        active_record.publish_status=True
        feature.publish_status=False
        return True

class InventiveFeatures(models.Model):
    _name="inventive.features"
    _description = "Inventive Features"

    name = fields.Char("Name", required=True)
    dynamic_snippet         = fields.Selection([('featured', 'Featured Products'),('tabs', 'Products Tabs')],string="Snippet Name", default='tabs')
    featured_product_type   = fields.Selection(
                                [('new','New Products'),('featured','Featured'),('rated','Top Rated')], string="Feature Products Type", default=False)
    tabs_product_type       = fields.Selection(
                                [('all','All'),('latest','Latest'),('sale','Popular')], string="Tab Products Type", default=False)
    auto_select             = fields.Boolean("Auto Products Selection",default=True)
    cron_id                 = fields.Many2one('ir.cron',string="Auto Select Cron",readonly=True)
    products                = fields.Many2many('product.template',  string="Featured Products", compute="_compute_products", search='_search_upper',store=True)
    publish_status          = fields.Boolean("Published",default=False)
    avg_rating              = fields.Float("Average Rating", default=1.0)
    products_limit          = fields.Integer("Limit",help="There should be a limit that how may products will be visible on website",default=5)

    _sql_constraints = [
        ('f_type_unique', 'UNIQUE (featured_product_type)',  'You can not have two features with same Feature Products type !'),
        ('t_type_unique', 'UNIQUE (tabs_product_type)',  'You can not have two features with same Tab Products type  !'),
    ]
    @api.model
    def create_feature_cron(self):
        model = self.env['ir.model'].sudo().search([('model','=','inventive.features')])
        name = self.name or "new"
        val = {
			"name":"Inventive Feature Auto Porduct Selection Cron",
			"active" :True,
			"user_id": self.env.user.id,
			"numbercall":-1,
			"doall":1,
			"model_id": model.id,
			"state":"code",
			"code":"model._auto_product_selection_cron()",
			"interval_number": 1,
			"interval_type":"days",
		}
        return self.env["ir.cron"].create(val)

    def unlink(self):
        res = super(InventiveFeatures , self).unlink()
        features = self.env["inventive.features"].search([])
        if not features:
            cron = self.env["ir.cron"].search([('name', '=' ,'Inventive Feature Auto Porduct selection cron')])
            cron.unlink()
        return res

    def _auto_product_selection_cron(self):
        features = self.env["inventive.features"].search([])
        for feature in features:
            feature._compute_products()

    def toggle_publish_status(self):
        if self.publish_status:
            self.publish_status=False
        else:
            records = self.env['inventive.features'].search([('featured_product_type','=',self.featured_product_type),('tabs_product_type','=',self.tabs_product_type)])
            f_type = self.featured_product_type if self.featured_product_type else self.tabs_product_type
            for feature in records:
                if feature.publish_status:
                    msg = "There is other feature with the same Feature Type (" + f_type + ") is already published if you publish this feature then that feature will be unpublished automatically. "
                    return self.show_msg_wizard(feature,msg)
            self.publish_status=True
            cron = self.env["ir.cron"].search([('name', '=' ,'Inventive Feature Auto Porduct Selection Cron')])
            self.cron_id = cron and cron.id or self.create_feature_cron().id

    def show_msg_wizard(self,feature,msg):
        res_id=self.env['wizard.feature.message'].create({'msg':msg})
        return {
                'domain': "[]",
                'name': 'Warning',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'wizard.feature.message',
                'type': 'ir.actions.act_window',
                'context': {'feature_id': feature.id},
                'res_id':res_id.id,
                'view_id': self.env.ref('theme_inventive.wizard_feature_warning_form_view').id,
                'target': 'new',
        }

    @api.depends("products_limit")
    def _compute_products(self):
        for feature in self:
            if not self.auto_select:
                continue
            else:
                if self.dynamic_snippet == "featured":
                    self.compute_featured_products()
                elif self.dynamic_snippet == "tabs":
                    self.compute_featured_tabs_products()
                else:
                    pass
    @api.onchange('tabs_product_type')
    def _tabs_products_type(self):
        if self.auto_select:
            self._compute_products()

    @api.onchange('featured_product_type')
    def _featured_products_type(self):
        if self.auto_select:
            self._compute_products()

    @api.onchange("auto_select")
    def reset_products(self):
        if self.auto_select:
            self._compute_products()
        else:
            self.products = False

    def compute_featured_products(self):
        if self.auto_select:
            try:
                f_type = self.featured_product_type
                limit = self.products_limit
                if f_type == 'new':
                    order ="create_date desc"
                elif f_type == 'featured':
                    order ="website_sequence desc"
                elif f_type == 'rated':
                    order ="product_avg_rating desc"
                else:
                    _logger.error("\n.........products.type Not Matched......................")
                domain = [('website_published','=',True)]
                products = self.env['product.template'].search(domain,order=order,limit=limit)
                if len(products):
                    self.products = products
            except Exception as e:
                _logger.error("\n+++++++++++++++++Error ++++___%r____+++++++++++++++",e)

    def compute_featured_tabs_products(self):
        if self.auto_select:
            try:
                f_type = self.tabs_product_type
                limit = self.products_limit
                if f_type == 'all':
                    order ="id desc"
                elif f_type == 'latest':
                    order ="create_date desc"
                elif f_type == 'sale':
                    order ="sales_count desc"
                else:
                    _logger.error("\n.........products.type Not Matched......................")
                domain = [('website_published','=',True)]
                products = self.env['product.template'].search(domain,order=order,limit=limit)
                if products:
                    self.products = products
            except Exception as e:
                _logger.error("\n+++++++++++++++++Error ++++___%r____+++++++++++++++",e)
