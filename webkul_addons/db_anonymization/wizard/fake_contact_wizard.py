# -*- coding: utf-8 -*-
################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
################################################################################
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError


class FakeContactWizard(models.TransientModel):
    _name = "fake.contact.wizard"

    def defaultTotalContact(self):
        count = self.env['res.partner'].sudo().search_count([('active','in',[False,True])])
        return count

    total_contact_count = fields.Integer(string='Total Contacts',default=defaultTotalContact,readonly=True)
    create_contact_count = fields.Integer(string='Fake Contacts No.',default=defaultTotalContact,required=True)
    database_backup_id = fields.Many2one('database.backup',string='Database Backup Id',required=True)

    def action_create_fake_record(self):
        self.env['faker.contact'].sudo().create_faker_contact(self.create_contact_count)
        self.database_backup_id.is_fake_created = True
