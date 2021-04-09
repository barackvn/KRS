# -*- coding: utf-8 -*-
#################################################################################
##    Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################
from odoo import api, fields, models
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
class ProductPricelist(models.Model):
    _inherit = "product.pricelist"
    def unlink(self):
        if self.name == "Deals Dummy Pricelist":
            raise Warning("This Pricelist Should not be deleted, Because this is used by module website Daily Deals for its operation")
        else:
            super(ProductPricelist,self).unlink()

    def write(self,vals):
        if self.name == "Deals Dummy Pricelist":
            pass
            #raise Warning("This Pricelist Should not be update, Because this is used by module website Daily Deals for its operation")
        else:
            super(ProductPricelist,self).write(vals)

class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    website_deals_m2o = fields.Many2one('website.deals', 'Corresponding Deal', help="My Deals", ondelete="cascade")
    actual_price = fields.Float(string='Actual Price', default="0.0")
    discounted_price = fields.Float('Discounted Price',default=0.0, readonly=True)
    website_size_x = fields.Integer('Size X',default=2)
    website_size_y = fields.Integer('Size Y',default=2)
    deal_applied_on = fields.Selection([('1_product', 'Product'),('0_product_variant', 'Product Variant')], "Apply On", help='Pricelist Item applicable on selected option')


    @api.onchange('deal_applied_on','product_tmpl_id','product_id')
    def onchange_deal_applied_on(self):
        self.applied_on = self.deal_applied_on
        self.pricelist_id = self.website_deals_m2o.deal_pricelist
        self.min_quantity = 1
        self._update_actual_price()

    @api.model
    def _update_actual_price(self):
        if self.applied_on=="1_product":
            self.actual_price = self.product_tmpl_id.list_price
        elif self.applied_on=="0_product_variant":
            self.actual_price = self.product_id.lst_price
        else:
            self.actual_price = 0.0
        self.discounted_price = 0.0
