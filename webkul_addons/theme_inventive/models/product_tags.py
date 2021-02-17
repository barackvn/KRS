from odoo import models, fields, api

class ThemeProductTags(models.Model):
    _name="th.product.tags"
    _description = "Product Tags"

    name=fields.Char("Name",required=True,translate=True)
    style = fields.Selection([
            ('style_1','Style 1'),
            ('style_2','Style 2'),
            ('style_3','Style 3'),
            ('style_4','Style 4'),
            ],"Styles",default="style_1")

    product_ids = fields.One2many(
        "product.template",
        "product_tag_id",
        string='Associated Product',
    )
    website_publish = fields.Boolean(
        string='Available in the website',
        default=True
    )
    def _get_active_tags(self):
        product_tag_ids = self.env['th.product.tags'].search([('website_publish','=',True)])
        return product_tag_ids.filtered(lambda tag : tag.product_ids)

    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'Tags must be Unique .')
    ]
    def toggle_publish_status(self):
        self.website_publish =  not self.website_publish

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    product_tag_id=fields.Many2one("th.product.tags","Sale Product Tag")
