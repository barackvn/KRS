# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import base64
import codecs
import csv
import io
import logging
import xlrd

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)
product = [
    'product_external_id', 'product_id', 'product_code', 'product_barcode'
]
location = ['location_external_id', 'location_id', 'location_name']
lot = ['lot_external_id', 'lot_id', 'lot_name']
file_type = ['csv', 'xls']


class InventoryImport(models.TransientModel):
    _name = "invetorty.import"
    _description = "Inventory Import"

    name = fields.Char(string="Inventory Reference", required="True")
    location_id = fields.Many2one(
        "stock.location",
        string="Location",
        domain="[('usage','=','internal')]",
    )
    import_type = fields.Selection([('csv', 'CSV'), ('xls', 'XLS')],
                                   string="Import As",
                                   default="csv",
                                   required=True)
    import_file = fields.Binary('File', required=True)
    import_lot = fields.Boolean(string="Import Using Lot Number")
    filename = fields.Char("Filename")

    @api.model
    def _wk_default_location_id(self):
        company_user = self.env.user.company_id
        warehouse = self.env['stock.warehouse'].search(
            [('company_id', '=', company_user.id)], limit=1)
        if warehouse:
            return warehouse.lot_stock_id.id
        else:
            raise UserError(
                _('You must define a warehouse for the company: %s.') % (company_user.name, ))

    @api.model
    def create(self, vals):
        if vals.get('import_file'):
            ext = vals.get('filename').split(".")
            if ext and ext[-1] != vals.get('import_type'):
                raise UserError(
                    "Could not find an %s file, please select a valid %s file"
                    % (vals.get('import_type'), vals.get('import_type')))
            if vals.get('import_type') == 'csv':
                zip_ref = base64.b64decode(vals['import_file'])

        return super(InventoryImport, self).create(vals)

    def import_stock(self):
        stock_inventory = self.env['stock.inventory']
        inventory_vals = {
            'name': self.name,
            'location_ids': self.location_id.ids if self.location_id else False,
            'start_empty': True
        }
        inventory = stock_inventory.create(inventory_vals)
        if not inventory.location_ids:
            inventory._onchange_company_id()
        inventory.action_start()
        line_ids = []
        message = ''
        if self.import_file:
            if self.import_type == 'csv':
                file = base64.b64decode(self.import_file)
                zip_input = io.BytesIO(file)
                reader = csv.reader(codecs.iterdecode(zip_input, 'utf-8'))
                header = next(reader)
                if not any(hed in product for hed in header):
                    raise UserError(_('Product Information Missing '))
                if 'quantity' not in header:
                    raise UserError(_("Quantity Missing"))
                if self.import_lot and not any(head in lot for head in header):
                    raise UserError(_('Lot information missing'))
                zip_input = io.BytesIO(file)
                data_dict = csv.DictReader(
                    codecs.iterdecode(zip_input, 'utf-8'))
                for data in data_dict:
                    result = self.create_data(data, header)
                    if result.get('values'):
                        vals = result.get('values')
                        vals['inventory_id'] = inventory.id
                        if not vals.get('location_id'):
                            vals['location_id'] = self.location_id.id if self.location_id else self._wk_default_location_id()
                        line_ids.append(vals)
                    message += "<br/>" + result.get('msg') if result.get('msg') else ''
            elif self.import_type == 'xls':
                header = []
                file = base64.b64decode(self.import_file)
                zip_input = io.BytesIO(file)
                wb = xlrd.open_workbook(file_contents=zip_input.getvalue())
                sheet = wb.sheet_by_index(0)
                sheet.cell_value(0, 0)
                for i in range(sheet.ncols):
                    header.append(sheet.cell_value(0, i))
                if not any(hed in product for hed in header):
                    raise UserError(_('Product Information Missing '))
                if 'quantity' not in header:
                    raise UserError(_("Quantity Missing"))
                if self.import_lot and not any(head in lot for head in header):
                    raise UserError(_('Lot information missing'))
                first_row = []  # The row where we stock the name of the column
                for col in range(sheet.ncols):
                    first_row.append(sheet.cell_value(0, col))
                # transform the workbook to a list of dictionaries
                data_list = []
                for row in range(1, sheet.nrows):
                    elm = {}
                    for col in range(sheet.ncols):
                        elm[first_row[col]] = sheet.cell_value(row, col)
                    data_list.append(elm)
                for data in data_list:
                    result = self.create_data(data, header)
                    if result.get('values'):
                        vals = result.get('values')
                        if not vals.get('location_id'):
                            vals['location_id'] = self.location_id.id if self.location_id else self._wk_default_location_id()
                        vals['inventory_id'] = inventory.id
                        line_ids.append(vals)
                    message += "<br/>" + result.get('msg') if result.get('msg') else ''
        for line in line_ids:
            self.env['stock.inventory.line'].create(line)
        if not message:
            message = "Update Successfully!!"
        return self.env['stock.inventory.wizard'].with_context({
            'inventory_id': inventory.id
        }).generated_message(message)

    def filter_header(self, header):
        product_filter = location_filter = lot_filter = (False, False)
        if 'product_external_id' in header:
            product_filter = ('product_external_id', 'external_id')
        elif 'product_id' in header:
            product_filter = ('product_id', 'id')
        elif 'product_code' in header:
            product_filter = ('product_code', 'default_code')
        elif 'product_barcode' in header:
            product_filter = ('product_barcode', 'barcode')
        if 'location_external_id' in header:
            location_filter = ('location_external_id', 'external_id')
        elif 'location_id' in header:
            location_filter = ('location_id', 'id')
        elif 'location_name' in header:
            location_filter = ('location_name', 'name')
        if 'lot_external_id' in header:
            lot_filter = ('lot_external_id', 'external_id')
        elif 'lot_id' in header:
            lot_filter = ('lot_id', 'id')
        elif 'lot_name' in header:
            lot_filter = ('lot_name', 'name')
        return product_filter, location_filter, lot_filter

    def create_data(self, data, header):
        result = {'status': True, 'msg': ''}
        product_filter, location_filter, lot_filter = self.filter_header(
            header)
        vals = data.copy()
        if product_filter:
            if product_filter[1] == 'external_id':
                product = self.env['ir.model.data'].xmlid_to_object(data.get(product_filter[0]))
                vals.pop(product_filter[0])
                if product:
                    if product.type == "product":
                        vals['product_id'] = product.id
                    else:
                        result['status'] = False
                        result['msg'] = "%s product with external_id %s is not stockable" % (
                                product.name, data.get(product_filter[0]))
                        return result
                else:
                    result['status'] = False
                    result['msg'] = "Invalid Product ID:- %s" % (data.get(product_filter[0]))
                    return result
            elif product_filter[1] == 'id':
                if data.get(product_filter[0]).isdigit():
                    product = self.env['product.product'].search([
                        (product_filter[1], '=', data.get(product_filter[0]))
                    ], limit=1)
                    vals.pop(product_filter[0])
                    if product:
                        if product.type == "product":
                            vals['product_id'] = product.id
                        else:
                            result['status'] = False
                            result['msg'] = "%s product with id %s is not stockable" % (
                                    product.name, data.get(product_filter[0]))
                            return result
                    else:
                        result['status'] = False
                        result['msg'] = "Product ID not found:- %s" % (
                            data.get(product_filter[0]))
                        return result
                else:
                    result['status'] = False
                    result['msg'] = "Invalid Product ID:- %s" % (data.get(
                        product_filter[0]))
                    return result
            elif product_filter[1] == 'default_code':
                product = self.env['product.product'].search(
                    [(product_filter[1], '=', data.get(product_filter[0]))], limit=1)
                vals.pop(product_filter[0])
                if product:
                    if product.type == "product":
                        vals['product_id'] = product.id
                    else:
                        result['status'] = False
                        result['msg'] = "%s product with Internal Reference %s is not stockable" % (
                                product.name, data.get(product_filter[0]))
                        return result
                else:
                    result['status'] = False
                    result['msg'] = "Invalid Internal Reference:- %s" % (data.get(product_filter[0]))
                    return result
            elif product_filter[1] == 'barcode':
                vals.pop(product_filter[0])
                product = self.env['product.product'].search(
                    [(product_filter[1], '=', data.get(product_filter[0]))], limit=1)
                if product:
                    if product.type == "product":
                        vals['product_id'] = product.id
                    else:
                        result['status'] = False
                        result['msg'] = "%s product with Barcode %s is not stockable" % (
                                product.name, data.get(product_filter[0]))
                        return result
                else:
                    result['status'] = False
                    result['msg'] = "Invalid barcode:- %s" % (data.get(product_filter[0]))
                    return result
        if location_filter:
            if location_filter[1] == 'external_id':
                location = self.env['ir.model.data'].xmlid_to_object(data.get(location_filter[0]))
                vals.pop(location_filter[0])
                if location:
                    vals['location_id'] = location.id
                else:
                    result['status'] = False
                    result['msg'] = "Invalid Location External ID:- %s" % (data.get(location_filter[0]))
            elif location_filter[1] == 'id':
                if data.get(location_filter[0]).isdigit():
                    location = self.env['stock.location'].search([
                        (location_filter[1], '=', data.get(location_filter[0]))
                    ], limit=1)
                    vals.pop(location_filter[0])
                    if location:
                        vals['location_id'] = location.id
                    else:
                        vals.pop(location_filter[0])
                        result['status'] = False
                        result['msg'] = "Invalid Location Id:- %s" % (data.get(location_filter[0]))
                else:
                    vals.pop(location_filter[0])
                    result['status'] = False
                    result['msg'] = "Wrong entry for location_id (%s) in CSV." % (data.get(location_filter[0]))
            elif location_filter[1] == 'name':
                location = self.env['stock.location'].search(
                    [(location_filter[1], '=', data.get(location_filter[0]))], limit=1)
                vals.pop(location_filter[0])
                if location:
                    vals['location_id'] = location.id
                else:
                    result['status'] = False
                    result['msg'] = "Invalid Location Name:- %s" % (data.get(location_filter[0]))
        if lot_filter and self.import_lot:
            if lot_filter[1] == 'external_id':
                lot = self.env['ir.model.data'].xmlid_to_object(data.get(lot_filter[0]))
                vals.pop(lot_filter[0])
                if lot:
                    vals['prod_lot_id'] = lot.id
                else:
                    result['status'] = False
                    result['msg'] = "Invalid Lot External ID:- %s" % (data.get(lot_filter[0]))
            elif lot_filter[1] == 'id':
                if data.get(lot_filter[0]).isdigit():
                    lot = self.env['stock.production.lot'].search(
                        [(lot_filter[1], '=', data.get(lot_filter[0]))], limit=1)
                    vals.pop(lot_filter[0])
                    if lot:
                        vals['prod_lot_id'] = lot.id
                    else:
                        result['status'] = False
                        result['msg'] = "Invalid Lot Id:- %s" % (data.get(lot_filter[0]))
                else:
                    vals.pop(lot_filter[0])
                    result['status'] = False
                    result['msg'] = "Invalid Lot Id:- %s" % (data.get(lot_filter[0]))
            elif lot_filter[1] == 'name':
                lot = self.env['stock.production.lot'].search(
                    [(lot_filter[1], '=', data.get(lot_filter[0]))], limit=1)
                if not lot:
                    lot = self.env['stock.production.lot'].create({
                        'name': data.get(lot_filter[0]),
                        'product_id': vals.get('product_id')
                    })
                vals.pop(lot_filter[0])
                vals['prod_lot_id'] = lot.id
        if data.get('quantity'):
            if type(data.get('quantity')) == str \
                and data.get('quantity').replace('.', '', 1).isdigit():
                vals['product_qty'] = float(data.get('quantity'))
                vals.pop('quantity')
            elif type(data.get('quantity')) in [float, int]:
                vals['product_qty'] = (data.get('quantity'))
                vals.pop('quantity')
            else:
                result['status'] = False
                result['msg'] = "Invalid Quantity:- %s" % (data.get('quantity'))
                return result
        result['values'] = vals
        return result
