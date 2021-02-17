# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import api,exceptions,fields,models

from datetime import date


class Reminder(models.Model):
	_name = 'reminder.reminder'
	_inherit = 'mail.thread'

	name        = fields.Char('Subject',required=True,track_visibility='onchange')
	date        = fields.Date('Remind Date',track_visibility='onchange')
	end_date    = fields.Date('Stop Date',track_visibility='onchange')
	description = fields.Html('Description')
	auto_email  = fields.Boolean('Auto Send Email',default=False)
	recipients  = fields.Many2many(
		comodel_name = 'res.users',
		string       = 'Recipients',
		required     = True,
		default      = lambda self: self.env.user,
	)
	mail_template = fields.Many2one(
		comodel_name = 'mail.template',
		string       = 'Mail Template',
		default      = lambda self: self.env.ref('odoo_reminder.mail_reminder'),
	)
	repeat = fields.Selection(
		[
			('0','Once'),
			('1','Daily'),
			('7','Weekly'),
			('30','Monthly'),
		]
	)

	
	@api.constrains('date')
	def deny_past_date(self):
		if self.date and self.date < date.today():
			raise exceptions.UserError('No past date! Unless you got a time-machine')

	
	@api.constrains('date','end_date')
	def deny_past_end_date(self):
		if self.date and self.end_date and self.date >= self.end_date :
			raise exceptions.UserError('End date must be later than date')

	@api.model
	def create(self,values):
		obj = super(Reminder,self).create(values)
		self.env['reminder.history'].create(
			{
				'reminder': obj.id,
				'date'    : obj.date,
				'state'   : 'scheduled' if obj.auto_email else 'draft',
			}
		)
		return obj

	def write(self,values):
		history = self.env['reminder.history'].search(
			[
				('reminder','=',self.id),
				('state','in',['draft','scheduled'])
			]
		)

		if 'auto_email' in values:
			if values['auto_email']:
				if history:
					history.write({'state':'scheduled'})
				else:
					self.env['reminder.history'].create(
						{
							'reminder': self.id,
							'date'    : self.date,
							'state'   : 'scheduled'
						}
					)
			else:
				if history:
					history.write({'state':'draft'})
				values['repeat']=False

		if 'date' in values:
			if history:
				history.write({'date':values['date']})
			elif self.auto_email:
				self.env['reminder.history'].create(
					{
						'reminder': self.id,
						'date'    : values['date'],
						'state'   : 'scheduled',
					}
				)
				
		if values.get('repeat') in [False,0]:
			values['end_date']=False

		return super(Reminder,self).write(values)


	def unlink(self):
		for rec in self:
			self.env['reminder.history'].search(
				[('reminder','=',rec.id)]
			).sudo().unlink()
		return super(Reminder,self).unlink()


	def clearHistory(self):
		return self.env['reminder.history'].search(
			[
				('reminder','=',self.id),
				('state','not in',['draft','scheduled'])
			]
		).sudo().unlink()
