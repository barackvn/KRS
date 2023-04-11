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

from odoo import models,fields,api
from odoo.exceptions import ValidationError,UserError
import logging
_logger = logging.getLogger(__name__)


class MassUploadSettings(models.Model):
    _name = "mass.upload.settings"
    _description = "Settings for mass uplaod"

    def _get_fields():
        return [
            'name',
            'lst_price',
            'type',
            'default_code',
            'categ_id',
            'barcode',
            'hs_code',
            'description_sale',
            'volume',
            'weight',
            'description_picking',
            'description_pickingout',
            'website_id',
            'sale_delay',
        ]
        
    name = fields.Char('Name',required="True")
    mass_import_fields = fields.Many2many("ir.model.fields","ir_model_fields_mass_upload_settings_rel",string="Choose CSV Fields", domain=[('model_id.model','=','product.template'),('name' ,'in', _get_fields())],required="True")
    is_required = fields.Boolean('Required',help="If required is True then all the fields are mandatory to include in CSV")
    active = fields.Boolean(string="Activate this settings")
    website_id = fields.Many2one(comodel_name="website",string="Website",required="True")



    @api.model
    def create(self,vals):
        
        if self._context.get("mass_upload_default_settings"):
            fields_rec = self.env['ir.model.fields'].search([('name','in',['name','lst_price','type']),('model_id.model','=','product.template')])

            ids = fields_rec.mapped('id')
            vals['mass_import_fields'] = [(6,0,ids)]

        prev_rec = self.search_count([('website_id','=',vals['website_id'])])
        if not prev_rec:
            vals['active'] = True
        return super(MassUploadSettings,self).create(vals)


    def unlink(self):
        for rec in self:
            if rec.active:
                raise UserError('You cannot delete active settings, make another settings active to delete this settings.')
        return super(MassUploadSettings, self).unlink()
 
    def activate_settings(self):
        for rec in self:
            rec.active = True
            record = self.sudo().search([('website_id','=',rec.website_id.id),('id','!=',rec.id),('active','=',True)])
            record.active = False

    def deactivate_settings(self):
        raise UserError('You cannot deactivate settings, you have to make active which you want and this will get inactive by default.')
    
