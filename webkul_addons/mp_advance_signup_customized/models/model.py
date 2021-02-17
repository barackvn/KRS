# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)

class PartnerSpeciality(models.Model):
    _name = 'partner.speciality'
    _description = 'speciality labels for partner'
    _order = 'sequence'

    sequence = fields.Integer(copy=False)
    name = fields.Char(string='Name',required=True, copy=False)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_speciality_id = fields.Many2one('partner.speciality', string='Speciality')

class Product(models.Model):
    _inherit = 'product.template'

    exclusively_id = fields.Many2one('partner.speciality', string='Exclusively')

        