# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import api,fields,models

from datetime import date,timedelta
from dateutil.relativedelta import relativedelta


def addMonth(sdate,rdate):
	i=0
	while True:
		i+=1
		ndate=rdate+relativedelta(months=i)
		if sdate < ndate:
			return ndate

class ReminderHistory(models.Model):
	_name = 'reminder.history'

	reminder = fields.Many2one('reminder.reminder',required = True)
	name     = fields.Char('Subject',related='reminder.name')
	repeat   = fields.Selection(related='reminder.repeat')
	date     = fields.Date()
	state    = fields.Selection(
		[
			('draft','Draft'),
			('scheduled','Scheduled'),
			('sent','Email Sent'),
			('fail','Email Failed'),
		],
		required = True,
		default  = 'draft',
	)

	def sendReminderEmails(self,retry=False):
		emails = list(filter(None,self.reminder.mapped('recipients.email')))

		if emails:
			mail_template = self.env.ref('odoo_reminder.mail_reminder')
			mail_template.email_to = ','.join(emails)

			if mail_template.send_mail(self.reminder.id,True):
				self.write({'state':'sent'})
			else:
				self.write({'state':'fail'})
		else:
			self.write({'state':'fail'})

		if self.repeat and not retry:
			if self.repeat == 30:
				schedule_date = addMonth(self.date,self.reminder.date)
			else:
				schedule_date = self.reminder.date + timedelta(days=self.repeat)
			if not self.reminder.end_date or schedule_date <= self.reminder.end_date:
				self.env['reminder.history'].create(
					{
						'reminder': self.reminder.id,
						'date'    : schedule_date,
						'state'   : 'scheduled',
					}
				)

	@api.model
	def periodicRemindersEmails(self):
		for history in self.search(
			[
				('state','=','scheduled'),
				('date','=',date.today())
			]
		):
			history.sendReminderEmails()
	

	def retryEmail(self):
		self.sendReminderEmails(True)
