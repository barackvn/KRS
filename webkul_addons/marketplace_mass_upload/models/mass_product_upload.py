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
import io, zipfile, os, ast
import csv
import logging
_logger = logging.getLogger(__name__)

class MassProductUpload(models.Model):
    _name = "mass.product.upload"
    _description = "Upload mass product"
    _order = "id desc"

    name = fields.Char('Filename')
    zip_file = fields.Binary('Zip File', required=True)
    seller_id = fields.Many2one(
        string="Marketplace Seller",
        comodel_name="res.partner",
        domain=[('seller', '=', True)],
        help="Marketplace seller",
        required = True,
        default=lambda self: self.env.user.partner_id.id if self.env.user.partner_id and self.env.user.partner_id.seller else self.env['res.partner']
    )

    note = fields.Text('Note')
    state = fields.Selection([('new','New'),('success','Success'),('partial','Partially Failed'),('fail','Failed')],default='new')
    fails = fields.Integer(default=0)
    passes = fields.Integer(default=0)
    description = fields.Text('Description')

    @api.model
    def create(self,vals):

        if vals.get('zip_file'):
            zip_ref = base64.b64decode(vals['zip_file'])
            zip_input = io.BytesIO(zip_ref)
            if not zipfile.is_zipfile(zip_input):
                raise UserError("Did not find zip file, please select zip file.")
        self.validate_header(vals['zip_file'])
        return super(MassProductUpload,self).create(vals)

    def validate_header(self,zip_file):
        zip,filenames = self.get_zipfile_obj(zip_file)
        headers,csv_dict = self.read_csv_file(zip,filenames)
        field_list,fields_required = self.get_fields_name()
        if fields_required:
            for field in field_list:
                if field not in headers:
                    raise UserError('Some Fields are mising. Please download the sample CSV to check the Fields.')
        return True

    
    def get_zipfile_obj(self,zip_file):
        zip_ref = base64.b64decode(zip_file)
        zip_input = io.BytesIO(zip_ref)
        zip = zipfile.ZipFile(zip_input,'r')
        files = zip.namelist()
        return zip,files

    def read_csv_file(self,zip,files):
        csv_data = False
        try:
            data = zip.open(files[1])
            csv_as_text = io.TextIOWrapper(data,'utf-8')
            csv_data = csv.DictReader(csv_as_text)
            headers = csv_data.fieldnames
            csv_data = list(csv_data)
        except Exception as e:
            raise ValidationError('Your CSV File is not in the correct Format')
        return headers,csv_data

    @api.model
    def get_image(self,img_name,zip,filenames):
        image_name = f'{filenames[0]}images/{img_name}'
        return zip.read(image_name) if image_name in filenames else False

    def get_fields_name(self):

        if website_id := self.env['website'].get_current_website().id:
            settings_fields = self.env['mass.upload.settings'].search_read([('active','=',True),('website_id','=',website_id)],['mass_import_fields','is_required'],limit=1)
        else:
            # If website_id not found then fetch last created active record
            settings_fields = self.env['mass.upload.settings'].search_read([('active','=',True)],['mass_import_fields','is_required'],limit=1, order="id desc")
        if not settings_fields:
            raise UserError('No settings defined yet.')

        ids = settings_fields[0].get('mass_import_fields')
        data = self.sudo().env['ir.model.fields'].search_read([('id','in',ids)],['name'])

        name_list = [name['name'] for name in data]
        # check name exist and it's index should be 0
        if 'name' not in name_list:
            name_list.insert(0,'name')
        elif name_list[0] != 'name':
            name_list.remove('name')
            name_list.insert(0,'name')
        # check image exist and it's index should be -1(last)
        if 'image' not in name_list:
            name_list.append('image')
        elif name_list[-1] != 'image':
            name_list.remove('image')
            name_list.append('image')

        return name_list,settings_fields[0].get('is_required')

    def get_m2m_fields(self,headers):
        return (
            self.sudo()
            .env['ir.model.fields']
            .search_read(
                [
                    ('name', 'in', headers),
                    ('model_id.model', '=', 'product.template'),
                    ('ttype', '=', 'many2many'),
                ],
                ['name', 'relation'],
            )
        )

    def get_m2o_fields(self,headers):
        return (
            self.sudo()
            .env['ir.model.fields']
            .search_read(
                [
                    ('name', 'in', headers),
                    ('model_id.model', '=', 'product.template'),
                    ('ttype', '=', 'many2one'),
                ],
                ['name', 'relation'],
            )
        )
        
    def get_m2m_field_ids(self,vals,m2m_fields):
        """This method checks the given many2many value is list and records of the given ids in the list exist"""
        
        user_given_list = False
        existed_rec = {}
        for field in m2m_fields:
            field_name = field['name']
            m2m_field_id_list = vals[field_name]
            if not m2m_field_id_list:
                continue
            elif m2m_field_id_list[0] != '[' and m2m_field_id_list[-1] != ']':
                continue 
            else:
                user_given_list = [int(i) for i in m2m_field_id_list.strip('[]').split(',') if i.isnumeric()]
            if user_given_list:
                rec = self.env[field['relation']].browse(user_given_list)
                ids_list = [record.id for record in rec.exists()]
                existed_rec[field_name] = ids_list
        return existed_rec

    def get_m2o_non_exis_rec(self,vals,m2o_fields):
        """This method checks the given many2one value is list and records of the given ids in the list exist"""

        non_existed_rec = {}
        for field in m2o_fields:
            field_name = field['name']
            m2o_field_id = vals[field_name]
            if not m2o_field_id or m2o_field_id and not m2o_field_id.isnumeric():
                non_existed_rec[field_name] = m2o_field_id
                continue
            else:
                int_id = int(m2o_field_id) if m2o_field_id.isnumeric() else m2o_field_id
                rec = self.env[field['relation']].browse(int_id)
                if not rec.exists():
                    non_existed_rec[field_name] = m2o_field_id
        return non_existed_rec

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
            status_msg = f'{self.passes} records have been created successfully.'

        status_rec = self.env['mass.upload.status'].create({'passed_rec':self.passes,'message':status_msg})
        return {
            'name': 'Mass Upload Wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'mass.upload.status',
            'view_mode': 'form',
            'res_id': status_rec.id,
            'target': 'new',
        }
        
   
    def upload_products(self):
        for record in self:
            zip,filenames = record.get_zipfile_obj(record.zip_file)
            headers,csv_dict = record.read_csv_file(zip,filenames)
            field_list,fields_required = record.get_fields_name()
            m2m_fields = record.get_m2m_fields(headers)
            m2o_fields = record.get_m2o_fields(headers)
            passed_rec = 0
            failed_rec = 0
            dscrptn = '____Failed_Records____'

            for vals in csv_dict:
                temp_dscrptn = list(vals.values())
                continue_loop = False

                # vals['name'] will be None when an empty line added in csv
                if vals['name'] == '' or vals['name'] is None:
                    continue_loop = True
                elif fields_required and '' in vals.values() or None in vals.values():
                    continue_loop = True
                if m2m_fields:
                    existed_rec = record.get_m2m_field_ids(vals,m2m_fields)
                    if existed_rec:
                        # if existed rec have valid values then it will be added to vals 
                        for key in existed_rec:
                            vals[key] = [(6,0,existed_rec[key])]

                    for val in m2m_fields:
                        # if any m2m field does not have any valid value or not present in existed_rec then delete the field from vals
                        if val['name'] not in existed_rec:
                            del vals[val['name']]

                if m2o_fields:
                    if non_existed_rec := record.get_m2o_non_exis_rec(
                        vals, m2o_fields
                    ):
                        if fields_required:
                            continue_loop = True
                        else:
                            for key in non_existed_rec:
                                del vals[key]

                if continue_loop:
                    failed_rec += 1
                    # check for list temp_dscrptn contains list at last index
                    if type(temp_dscrptn[-1]) == list:
                        list_data = temp_dscrptn[-1]
                        temp_dscrptn.pop(-1)
                        temp_dscrptn.extend(list_data)
                    # remove multiple None value appended by csv reader in dict values
                    for _ in range(len(temp_dscrptn)):
                        if None in temp_dscrptn:
                            temp_dscrptn.remove(None)
                        else:
                            break
                    dscrptn += '\n' + ','.join(temp_dscrptn)
                    continue

                try:   
                    if img_name := vals['image']:
                        image = record.get_image(img_name,zip,filenames)
                        vals['image_1920'] = base64.b64encode(image)
                    vals['marketplace_seller_id'] = record.seller_id.id
                    del vals['image']
                    if vals.__contains__(None):
                        del vals[None]

                    product = self.env['product.template'].create(vals)

                    product.auto_approve()
                    passed_rec += 1
                except Exception as e:
                    _logger.info("=========Exception===============%r",e)
                    failed_rec += 1
                    """check in any case except executes then all the values in list temp_dscrptn is string so that those values can be added in failed records message"""
                    appnd_dscrptn = all(type(i) == str for i in temp_dscrptn)
                    if appnd_dscrptn:
                        dscrptn += '\n' + ','.join(temp_dscrptn)

            record.passes = passed_rec
            record.fails = failed_rec
            record.description = dscrptn
            return_action = record.status_action()

        return return_action




    

