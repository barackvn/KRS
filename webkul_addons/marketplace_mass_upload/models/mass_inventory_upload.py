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

from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError
import base64
import io
import csv
import logging
_logger = logging.getLogger(__name__)

class MassInventoryUpload(models.Model):
    _name = "mass.inventory.upload"
    _description = "Update inventory of mass products"
    _rec = "csv_file"
    _order = "id desc"


    name = fields.Char('Filename')
    csv_file = fields.Binary('CSV File',required = True)
    seller_id = fields.Many2one(
        string="Marketplace Seller",
        comodel_name="res.partner",
        domain=[('seller', '=', True)],
        required = True,
        help="Marketplace seller",
        default=lambda self: self.env.user.partner_id.id if self.env.user.partner_id and self.env.user.partner_id.seller else self.env['res.partner']
    )
    note = fields.Text('Note')
    state = fields.Selection([('new','New'),('success','Success'),('partial','Partially Failed'),('fail','Failed')],default='new')
    fails = fields.Integer(default=0)
    passes = fields.Integer(default=0)
    description = fields.Text('Description')
    
    @api.constrains('name')
    def _check_file_type(self):
        name_list = self.name.split('.')
        if name_list[-1] != 'csv':
            raise ValidationError('Please upload csv file only')

    @api.model
    def create(self,vals):
        self.validate_header(vals['csv_file'])
        
        vals = super(MassInventoryUpload,self).create(vals)
        return vals

    def validate_header(self,csv_file):
        required_header = ['variant_id','default_code','quantity']
        headers,csv_data = self.read_csv_file(csv_file)
        # count is used to check 'variant_id','default_code','quantity' is in the same order
        count = 0
        for value in headers:
            if value != required_header[count]:
                raise UserError('Your CSV File is not in the correct Format. Please download sample CSV.')
            count += 1
        return True        
 

    def read_csv_file(self,csv_file):
        csv_data = []
        headers = False
        try:
            data = base64.b64decode(csv_file)
            # get first line of csv file as a list
            headers = data.splitlines()[0].decode('ascii').split(',')

            for lines in data.splitlines()[1:]:
                csv_data.append(lines.decode('ascii').split(','))            
        except Exception as e:
            _logger.info("=========EXCEPTION===============%r",e)
            raise UserError('Your CSV File is not in the correct Format. Please download sample CSV.')
        return headers,csv_data

    def status_action(self):
        status_msg = ''
        if self.passes == 0:
            self.state = 'fail'
            status_msg = "None of the records have been created."
        elif self.fails == 0:
            self.state = 'success'
            status_msg = 'All the records have been created successfully.'
        else:
            self.state = 'partial'
            status_msg = '{} records have been created successfully.'.format(self.passes)
            
        status_rec = self.env['mass.upload.status'].create({'passed_rec':self.passes,'message':status_msg})
        return_action = {
                'name' : 'Mass Upload Wizard',
                'type': 'ir.actions.act_window',
                'res_model': 'mass.upload.status',
                'view_mode': 'form',
                'res_id': status_rec.id,
                'target' : 'new'
        }

        return return_action

    def uploadInventory(self):
        for record in self:
            headers,csv_data = record.read_csv_file(record.csv_file)
            passed = 0
            failed = 0
            dscrptn = '____Failed_Records____'
            
            for line in csv_data:
                # if len(line) < 3 then comma separation is not correct
                if len(line) < 3:
                    failed += 1
                    dscrptn += '\n' + ','.join(line)
                    continue
                
                product_id, default_code, new_quantity= line[0], line[1], line[2]

                if new_quantity == '' or not new_quantity.isnumeric():
                    failed += 1
                    dscrptn += '\n' + ','.join(line)
                    continue
                
                seller_product = False
                if product_id != '' and product_id.isnumeric():
                    seller_product = self.env['product.product'].search([('id','=',int(product_id)),('marketplace_seller_id','=',record.seller_id.id)],limit=1)
                if not seller_product and default_code != '':
                    seller_product = self.env['product.product'].search([('default_code','=',default_code),('marketplace_seller_id','=',record.seller_id.id)],limit=1)

                if seller_product:
                    values = {
                        'product_id' : seller_product.id,
                        'new_quantity' : new_quantity,
                        'location_id' : record.seller_id.get_seller_global_fields('location_id'),
                        'note' : record.note,
                    }
                        
                    new_stock_inventory = self.env['marketplace.stock'].create(values)
                    if new_stock_inventory:
                        new_stock_inventory.request()
                        passed += 1
                else:
                    failed += 1
                    dscrptn += '\n' + ','.join(line)     

            record.passes = passed
            record.fails = failed
            record.description = dscrptn
            return_action = record.status_action()

        return return_action

    
    

    