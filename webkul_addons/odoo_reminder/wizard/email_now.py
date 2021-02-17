# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import api,fields,models

from datetime import date


class EmailNow(models.TransientModel):
	_name = 'email.now'

	mail_template = fields.Many2one(
		comodel_name = 'mail.template',
		string       = 'Mail Template',
		default      = lambda self: self.env.ref('odoo_reminder.mail_reminder'),
	)


	def emailNow(self):
		current_date = date.today()
		for reminder in self.env['reminder.reminder'].browse(
			self.env.context.get('active_ids')
		):
			emails = list(filter(None,reminder.mapped('recipients.email')))

			if emails:
				mail_template = self.mail_template
				mail_template.email_to = ','.join(emails)

				if mail_template.send_mail(reminder.id,True):
					self.env['reminder.history'].create(
						{
							'reminder': reminder.id,
							'date'    : current_date,
							'state'   : 'sent',
						}
					)
				else:
					self.env['reminder.history'].create(
						{
							'reminder': reminder.id,
							'date'    : current_date,
							'state'   : 'fail',
						}
					)
			else:
				self.env['reminder.history'].create(
					{
						'reminder': reminder.id,
						'date'    : current_date,
						'state'   : 'fail',
					}
				)
