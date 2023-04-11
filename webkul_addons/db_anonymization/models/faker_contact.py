# -*- coding: utf-8 -*-
#################################################################################
# Author : Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>;
#################################################################################
from odoo import models, fields,api,_
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError
import random
import string

from faker import Faker

def _default_unique_key(size, chars=string.digits):
	return ''.join(random.choice(chars) for _ in range(size))



class FakerContact(models.Model):
	_name = 'faker.contact'

	name = fields.Char(string="Name")
	city = fields.Char(string="City")
	email = fields.Char(string="Email")
	mobile = fields.Char(string="Mobile")
	phone = fields.Char(string="Phone")
	street = fields.Char(string="Street")
	street2 = fields.Char(string="street2")
	zip = fields.Char(string="Zip")
	website = fields.Char(string="Website")

	@api.model
	def create_faker_contact(self,count=0):
		fake = Faker()
		if not count :
			count = self.env['res.partner'].sudo().search_count([('active','in',[False,True])])
		_logger.info("<== CREATE %r FAKE RECORDS ==>",count)
		for _ in range(count):
			vals = {'name': fake.name()}
			vals['street'] = fake.address()
			vals['city'] = fake.city()
			vals['street2'] = vals['street'] + " " + vals['city']
			vals['email'] = fake.email()
			vals['zip'] = _default_unique_key(6)
			vals['phone'] =  _default_unique_key(6)
			vals['mobile'] = _default_unique_key(10)
			vals['website'] = fake.url()
			try:
				self.create(vals)
			except Exceptions as e:
				_logger.info(f"<EXCEPTION WHILE CREATE FAKE RECORD : {str(e)} >")

		_logger.info("<== END CREATE FAKE RECORD ==>")
