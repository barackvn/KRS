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
from odoo.exceptions import UserError

class LabCenters(models.Model):
    _name = 'patho.lab.centers'
    _description = "Pathology Centers"

    image = fields.Binary("Lab Center Image")
    name = fields.Char(string='Lab Name', required=True)
    is_lab_center = fields.Boolean("Is a Lab Center")
    is_collection_center = fields.Boolean("Is a Collection Center")
    phone = fields.Char('Mobile Number')
    email = fields.Char('Email Id')
    street1 = fields.Char("Street")
    city = fields.Char("City")
    zipcode = fields.Char("ZipCode")
    state_id = fields.Many2one('res.country.state',"State")
    country_id = fields.Many2one('res.country', related='state_id.country_id', string="Country")
    primary_labcenter_id = fields.Many2one('patho.lab.centers', 'Primary Laboratory Center',
        help="Lab Center where the samples of this collection center will be send.",
        domain= "[('is_lab_center', '=', True)]")
    primary_lab_pathologist = fields.Many2one('res.partner', "Primary Lab Pathologist", domain="[('pathologist','=',True)]",
        help="Select the Pathologist for this Collection Center")
    collection_center_ids = fields.Many2many('patho.lab.centers','lab_center_id', 'collection_id', 'lab_center_collection_table')
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide this record without removing it.")

    @api.onchange('is_lab_center')
    def on_change_is_lab_center(self):
        if self.is_lab_center ==  False and self.is_collection_center == False:
            self.is_collection_center = True

    @api.onchange('is_collection_center')
    def on_change_is_collection_center(self):
        if self.is_collection_center == False and self.is_lab_center == False:
            self.is_lab_center = True
