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
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    comm_method = fields.Selection([
        ('percent','Percent(%)'),
        ('fix','Fixed'),
        ('percent_and_fix','% + Fixed'),
        ('fix_and_percent','Fixed + %')],
        string="Commission Method",
        read=['odoo_marketplace.marketplace_seller_group'],write=['odoo_marketplace.marketplace_officer_group'],
        copy=False
    )
    percent_commission = fields.Float(string= 'Percent Commission',
        read=['odoo_marketplace.marketplace_seller_group'],write=['odoo_marketplace.marketplace_officer_group'],
        copy=False
    )
    fix_commission = fields.Float(string= 'Fixed Commission',
        read=['odoo_marketplace.marketplace_seller_group'],write=['odoo_marketplace.marketplace_officer_group'],
        copy=False
    )

    @api.model
    def create(self, vals):
        return super(ProductTemplate, self).create(vals)
    
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        for rec in self:
            rec._check_commission_values(vals)
        return res

    def _check_commission_values(self, vals):
        for rec in self:
            list_price = vals.get('list_price') or rec.list_price
            product_curr_id = vals.get('currency_id') or rec.currency_id
            config_currency = self.env['res.currency'].search([('id','=',(self.env['ir.default'].get('res.config.settings', 'mp_currency_id')))])

            if len(config_currency) == 0 :
                config_currency = self.env['res.currency'].search([('id', '=', rec.company_id.currency_id.id)])

            # Checking Product Commission
            comm_method = vals.get('comm_method') or rec.comm_method
            fix_comm = vals.get('fix_commission') or rec.fix_commission
            percent_comm = vals.get('percent_commission') or rec.percent_commission
            rec.calc_commission(comm_method, list_price, percent_comm, fix_comm)

            # Checking Category Commission
            public_categ_ids = vals.get('public_categ_ids') or rec.public_categ_ids
            if (
                isinstance(public_categ_ids, list)
                and public_categ_ids
                and public_categ_ids[0]
                and public_categ_ids[0][0]
                and public_categ_ids[0][0] == 6
                and public_categ_ids[0][2]
            ):
                for category in public_categ_ids[0][2]:
                    category_obj = self.env['product.public.category'].search([('id','=',category)])
                    category_list_price = product_curr_id.compute(list_price, config_currency)
                    rec.calc_commission(category_obj.comm_method, category_list_price, category_obj.percent_commission, category_obj.fix_commission, category=True)
                if public_categ_ids[0][0] and public_categ_ids[0][0]==4 and public_categ_ids[0][1]:
                    category =  public_categ_ids[0][1]
                    category_obj = self.env['product.public.category'].search([('id','=',category)])
                    category_list_price = product_curr_id.compute(list_price, config_currency)
                    rec.calc_commission(category_obj.comm_method, category_list_price, category_obj.percent_commission, category_obj.fix_commission, category=True)


            # Checking Seller Commission
            seller_obj = False
            if vals.get('marketplace_seller_id'):
                seller_obj = self.env['res.partner'].browse(vals.get('marketplace_seller_id'))
            elif rec.marketplace_seller_id:
                seller_obj = rec.marketplace_seller_id
            if seller_obj:
                seller_list_price = product_curr_id.compute(list_price, config_currency)
                rec.calc_commission(seller_obj.get_seller_global_fields('comm_method'), seller_list_price, seller_obj.get_seller_global_fields('commission'), seller_obj.get_seller_global_fields('fix_commission'), seller=True)
            return True


    def calc_commission(self, comm_method, list_price, percent_comm, fix_comm, category=None, seller=None):
        if comm_method:
            # Case Fix Commission
            if (
                comm_method in ['fix', 'percent_and_fix', 'fix_and_percent']
                and fix_comm > list_price
            ):
                if category:
                    raise ValidationError(_('Sale Price of product must be greater than value of Fixed Commission defined in selected Category.'))
                elif seller:
                    raise ValidationError(_('Sale Price of product must be greater than value of Fixed Commission defined in seller profile.'))
                else:
                    raise ValidationError(_('Sale Price of product must be greater than value of Fixed Commission of product.'))

            # Case Percent+Fix Commission
            if comm_method == 'percent_and_fix':
                percent_value = (list_price * (percent_comm / 100.0))
                comm_factor = percent_value + fix_comm
                if comm_factor > list_price:
                    if category:
                        raise ValidationError(_('Sale Price of product must be greater than value of % + Fixed Commission defined in selected Category.'))
                    elif seller:
                        raise ValidationError(_('Sale Price of product must be greater than value of % + Fixed Commission defined in Seller profile.'))
                    else:
                        raise ValidationError(_('Sale Price of product must be greater than value of % + Fixed Commission of product.'))

            # Case Fix+Percent Commission
            if comm_method == 'fix_and_percent' :
                fix_value = list_price - fix_comm
                percent_value = (fix_value * (percent_comm / 100.0))
                comm_factor = fix_comm + percent_value
                if comm_factor > list_price:
                    if category:
                        raise ValidationError(_('Sale Price of product must be greater than value of Fixed + %  Commission in selected Category.'))
                    elif seller:
                        raise ValidationError(_('Sale Price of product must be greater than value of Fixed + %  Commission defined in Seller profile.'))
                    else:
                        raise ValidationError(_('Sale Price of product must be greater than value of Fixed + %  commission of product.'))

        return 0
