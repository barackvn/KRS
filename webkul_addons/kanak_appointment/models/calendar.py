# -*- coding: utf-8 -*-
import math
import pytz
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import Warning


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    type = fields.Selection([('appointment', 'Appointment'), ('exception', 'Exception')], 'Type')
    number_of_days_temp = fields.Float(compute="_compute_no_of_days", string='No. of Days')

    @api.depends('start_datetime', 'stop_datetime')
    def _compute_no_of_days(self):
        for rec in self:
            if (rec.start_datetime and rec.stop_datetime) and (rec.start_datetime <= rec.stop_datetime):
                diff_day = rec._get_number_of_days(rec.start_datetime, rec.stop_datetime)
                rec.number_of_days_temp = round(math.floor(diff_day)) + 1
            else:
                rec.number_of_days_temp = 0

    app_partner_id = fields.Many2one(comodel_name="res.partner", string="Meeting With", default=lambda self: self.env.user.partner_id)
    app_date = fields.Datetime("Appointment Datetime")
    app_time = fields.Char("Appointment Time")
    app_duration = fields.Char("Duration")
    date_appointment = fields.Char("Date format in user timezone")
    app_tz = fields.Char('timezone', default=lambda self: self.app_partner_id.tz)
    app_state = fields.Selection([('pending', 'Pending'), ('cancel', 'Cancel'), ('done', 'Done')], string="Appointment State", default="pending")

    def _get_number_of_days(self, date_from, date_to):
        """Returns a float equals to the timedelta between two dates given as string."""
        from_dt = fields.Datetime.from_string(date_from)
        to_dt = fields.Datetime.from_string(date_to)
        diff = to_dt - from_dt
        diff_day = diff.days + float(diff.seconds) / 86400
        return diff_day

    def write(self, values):
        for rec in self:
            if self.start and not self.start_datetime:
                values['start_datetime'] = fields.Datetime.to_string(self.app_partner_id.get_utc_date(fields.Datetime.from_string(self.start), self.app_partner_id.tz))
            if self.stop and not self.stop_datetime:
                values['stop_datetime'] = fields.Datetime.to_string(self.app_partner_id.get_utc_date(fields.Datetime.from_string(self.stop), self.app_partner_id.tz))
        return super(CalendarEvent, self).write(values)

    @api.constrains('start_datetime', 'stop_datetime')
    def _check_date(self):
        for ex in self:
            if ex.type == 'exception':
                domain = [
                    ('start_datetime', '<', ex.stop_datetime),
                    ('stop_datetime', '>', ex.start_datetime),
                    ('app_partner_id', '=', ex.app_partner_id.id),
                    ('id', '!=', ex.id),
                    ('type', '=', 'exception')
                ]
            elif ex.type == 'appointment':
                domain = [
                    ('start_datetime', '<', ex.stop_datetime),
                    ('stop_datetime', '>', ex.start_datetime),
                    ('app_partner_id', '=', ex.app_partner_id.id),
                    ('id', '!=', ex.id),
                    ('type', '=', 'appointment')
                ]
            try:
                nex = self.search_count(domain)
            except:
                nex = 0
            if nex:
                raise Warning(_('You can not have 2 exceptions that overlaps on same day!'))
        return True

    @api.onchange('type')
    def on_change_type(self):
        if self.type == 'appointment':
            self.allday = False

    @api.model
    def create(self, vals):
        if vals.get('start_datetime') and not vals.get('app_date') and vals.get('type') == 'appointment':
            appointment_with = self.env['res.partner'].browse(vals.get('app_partner_id'))
            utc_date = fields.Datetime.from_string(vals.get('start_datetime'))
            date = appointment_with.get_tz_date(utc_date, appointment_with.tz)
            vals.update({
                'app_date': utc_date,
                'app_time': str(utc_date.strftime('%H:%M')),
                'date_appointment': str(date.strftime('%A, %B %d, %Y %H:%M')),
                'app_duration': str(timedelta(minutes=int(appointment_with.minutes_slot)))[0:4],
                'stop_datetime': fields.Datetime.to_string((utc_date + timedelta(minutes=int(appointment_with.minutes_slot)))),
            })
        return super(CalendarEvent, self).create(vals)


class CalendarAttendee(models.Model):

    _inherit = 'calendar.attendee'

    def get_user_tz_date(self):
        self.ensure_one()
        to_zone = pytz.timezone(self.partner_id.tz)
        from_zone = pytz.timezone('UTC')
        return from_zone.localize(fields.Datetime.from_string(self.event_id.app_date)).astimezone(to_zone)

    def _send_mail_to_attendees(self, template_xmlid, force_send=False, force_event_id=None):
        if(template_xmlid == 'calendar.calendar_template_meeting_reminder'):
            template_xmlid = 'kanak_appointment.calendar_template_meeting_kanak_invitation'
        if(template_xmlid == 'calendar.calendar_template_meeting_changedate'):
            template_xmlid = 'kanak_appointment.calendar_template_meeting_kanak_changedate'
        return super(CalendarAttendee, self)._send_mail_to_attendees(template_xmlid, force_send, force_send)