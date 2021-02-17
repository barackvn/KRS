# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo.tests import common

from datetime import date,timedelta


class TestReminder(common.TransactionCase):
	post_install = True
	
	def test_Reminder(self):

		start_date = date.today()
		end_date   = date.today()+timedelta(1)

		# Create Reminder
		reminder = self.env['reminder.reminder'].create(
			{
				'name'       :'Reminder Title',
				'description':'<b>Reminder</b> Description',
				'date'       :start_date,
				'auto_email' :True,
				'repeat'     :1,
				'end_date'   :end_date
			}
		)
		history = self.env['reminder.history'].search(
			[
				('reminder','=',reminder.id),
				('state','=','scheduled')
			]
		)
		self.assertTrue(history)

		# Send Reminder and reschedule
		history.sendReminderEmails()
		history = self.env['reminder.history'].search(
			[
				('reminder','=',reminder.id),
				('state','!=','sent')
			]
		)
		self.assertTrue(history)
		history = self.env['reminder.history'].search(
			[
				('reminder','=',reminder.id),
				('state','=','scheduled')
			]
		)
		self.assertEqual(history.date,end_date)

		# Send reminder and not reschedule because of end_date
		history.sendReminderEmails()
		history = self.env['reminder.history'].search(
			[
				('reminder','=',reminder.id),
				('state','=','scheduled')
			]
		)
		self.assertFalse(history)

		# Reschedule outdated reminder
		reminder.write(
			{
				'date'    : end_date,
				'end_date': False,
			}
		)
		history = self.env['reminder.history'].search(
			[
				('reminder','=',reminder.id),
				('state','=','scheduled')
			]
		)
		self.assertTrue(history)

		# Clear reminder history
		reminder.clearHistory()
		history = self.env['reminder.history'].search(
			[
				('reminder','=',reminder.id),
				('state','=','sent')
			]
		)
		self.assertFalse(history)

		# Disable reminder auto_email
		reminder.write({'auto_email':False})
		history = self.env['reminder.history'].search(
			[
				('reminder','=',reminder.id),
				('state','=','draft')
			]
		)
		self.assertTrue(history)

		# Delete reminder and associated histories
		reminder.unlink()
		history = self.env['reminder.history'].search([('reminder','=',reminder.id)])
		self.assertFalse(history)


	def test_ReminderMonthly(self):

		start_date = date(2100,1,31)
		end_date   = date(2100,6,5)

		# Create Reminder
		reminder = self.env['reminder.reminder'].create(
			{
				'name'       :'Reminder Title',
				'description':'<b>Reminder</b> Description',
				'date'       :start_date,
				'auto_email' :True,
				'repeat'     :30,
				'end_date'   :end_date
			}
		)
		history = self.env['reminder.history'].search(
			[
				('reminder','=',reminder.id),
				('state','=','scheduled')
			]
		)
		self.assertTrue(history)

		# Send Reminder and reschedule
		history.sendReminderEmails()
		history = self.env['reminder.history'].search(
			[
				('reminder','=',reminder.id),
				('state','!=','sent')
			]
		)
		self.assertTrue(history)
		history = self.env['reminder.history'].search(
			[
				('reminder','=',reminder.id),
				('state','=','scheduled')
			]
		)
		self.assertEqual(history.date,date(2100,2,28))

		# Send reminder and reschedule again
		history.sendReminderEmails()
		history = self.env['reminder.history'].search(
			[
				('reminder','=',reminder.id),
				('state','=','scheduled')
			]
		)
		self.assertEqual(history.date,date(2100,3,31))
