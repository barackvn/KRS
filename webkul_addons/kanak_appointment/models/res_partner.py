# -*- coding: utf-8 -*-
import pytz
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def get_tz(self):
        # put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
        return [tz for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]

    def get_tz_offset(self, name):
        return datetime.now(pytz.timezone(name or self.env.user.tz)).strftime('%z')

    team_member = fields.Boolean("Team Member Available For Appointment")
    mon = fields.Boolean("Monday")
    mon_from = fields.Float("AM")
    mon_to = fields.Float("PM")
    tue = fields.Boolean("Tuesday")
    tue_from = fields.Float("AM")
    tue_to = fields.Float("PM")
    wed = fields.Boolean("Wednesday")
    wed_from = fields.Float("AM")
    wed_to = fields.Float("PM")
    thu = fields.Boolean("Thursday")
    thu_from = fields.Float("AM")
    thu_to = fields.Float("PM")
    fri = fields.Boolean("Friday")
    fri_from = fields.Float("AM")
    fri_to = fields.Float("PM")
    sat = fields.Boolean("Saturday")
    sat_from = fields.Float("AM")
    sat_to = fields.Float("PM")
    sun = fields.Boolean("Sunday")
    sun_from = fields.Float("AM")
    sun_to = fields.Float("PM")
    minutes_slot = fields.Integer("Slot in mins.")
    lunch_start = fields.Float("Lunch Start")
    lunch_end = fields.Float("Lunch End")
    exraoffset = fields.Float(compute='_get_extraoffset', store=True)
    min_date = fields.Date()
    max_date = fields.Date()

    @api.depends('mon_from', 'mon_to', 'tue_from', 'tue_to', 'wed_from', 'wed_to',
                 'thu_from', 'thu_to', 'fri_from', 'fri_to', 'sat_from', 'sat_to', 'sun_from', 'sun_to')
    def _get_extraoffset(self):
        for rec in self:
            if rec.mon and rec.mon_from % 1 > 0:
                rec.exraoffset = rec.mon_from % 1
            elif rec.tue and rec.tue_from % 1 > 0:
                rec.exraoffset = rec.mon_from % 1
            elif rec.wed and rec.wed_from % 1 > 0:
                rec.exraoffset = rec.mon_from % 1
            elif rec.thu and rec.thu_from % 1 > 0:
                rec.exraoffset = rec.thu_from % 1
            elif rec.fri and rec.fri_from % 1 > 0:
                rec.exraoffset = rec.mon_from % 1
            elif rec.sat and rec.sat_from % 1 > 0:
                rec.exraoffset = rec.sat_from % 1
            elif rec.sun and rec.sun_from % 1 > 0:
                rec.exraoffset = rec.sun_from % 1

    appointment_ids = fields.One2many(comodel_name="calendar.event", inverse_name="app_partner_id", string="exceptions", domain=[('type', '=', 'appointment')])
    exception_ids = fields.One2many(comodel_name="calendar.event", inverse_name="app_partner_id", string="exceptions", domain=[('type', '=', 'exception')])

    @api.model
    def get_tz_date(self, date=None, timezone=None):
        to_zone = pytz.timezone(timezone)
        from_zone = pytz.timezone('UTC')
        return from_zone.localize(date).astimezone(to_zone)

    @api.model
    def get_utc_date(self, date=None, timezone=None):
        to_zone = pytz.timezone('UTC')
        from_zone = pytz.timezone(timezone)
        return from_zone.localize(date).astimezone(to_zone)

    @api.model
    def string_to_minutes(self, minutes=None):
        minutes_str = minutes.split(":")
        return (int(minutes_str[0])*60) + (int(minutes_str[1]))

    @api.model
    def minutes_to_string(self, minutes=None):
        minutes_str = str(minutes / 60.0).split(".")
        return "%02d:%02d" % (int(minutes_str[0]), int(minutes_str[1]) * 6)

    @api.model
    def get_range(self, start, stop, step):
        r = start
        while r < stop:
            a = str(float(r)).split('.')
            my_time = int(a[1])
            yield "%02d:%02d" % (int(a[0]), my_time > 9 and (my_time * 6) / 10 or (my_time * 6))
            r += step

    @api.model
    def get_minutes(self, offset):
        return (float(offset) * 60) / 100

    def value_to_string_html(self, value):
        hours, minutes = divmod(abs(value) * 60, 60)
        minutes = round(minutes)
        if minutes == 60:
            minutes = 0
            hours += 1
        if value < 0:
            return '-%02d:%02d' % (hours, minutes)
        return '%02d:%02d' % (hours, minutes)

    def get_daily_slots(self, start, end, slot, date, partner, timezone):
        dt = datetime.combine(date, datetime.strptime(start, "%H:%M").time())
        utc_date = self.get_utc_date(dt, partner.tz)
        dtime = datetime.strptime(utc_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT), DEFAULT_SERVER_DATETIME_FORMAT)
        tz_time = self.get_tz_date(dtime, timezone)
        dt = tz_time
        slots = []
        slots.append(dt.strftime('%H:%M'))
        while (dt.time() < datetime.strptime(end, "%H:%M").time()):
            dt = dt + timedelta(minutes=slot)
            slots.append(dt.strftime('%H:%M'))
        return slots

    def get_book_info_slots(self, start, slot, duration):
        dt = datetime.combine(start.date(), datetime.strptime(str(start), DEFAULT_SERVER_DATETIME_FORMAT).time())
        new_dur = ((duration /60 ) * 60) - 1
        end = start + timedelta(minutes=new_dur)
        slots = []
        while (dt.time() <= end.time()):
            slots.append(dt.strftime('%H:%M'))
            dt = dt + timedelta(minutes=slot)
        return slots

    def get_booked_time(self, start_date, offset_min, timezone):
        self.ensure_one()
        user_today_appointment = []
        partner_appointment = self.appointment_ids.filtered(lambda app: app.app_state == 'pending' or app.app_state == 'done')
        if partner_appointment:
            for my_appointment in partner_appointment:
                my_appointment_datetime = self.get_tz_date(datetime.strptime(str(my_appointment.app_date), DEFAULT_SERVER_DATETIME_FORMAT), timezone)
                my_appoint_date = my_appointment_datetime.strftime(DEFAULT_SERVER_DATE_FORMAT)
                tody_date = start_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
                if my_appoint_date == tody_date:
                        total_min = self.string_to_minutes(my_appointment_datetime.strftime('%H:%M'))
                        dims = my_appointment.stop - my_appointment.start
                        duration = dims.seconds/60
                        start_tz_time = self.get_tz_date(my_appointment.start, timezone).replace(tzinfo=None)
                        end_tz_time = self.get_tz_date(my_appointment.stop, timezone).replace(tzinfo=None)
                        my_appointment_range = self.get_book_info_slots(start_tz_time, self.minutes_slot, duration)
                        user_today_appointment = user_today_appointment + [a for a in my_appointment_range]
        return user_today_appointment

    def get_exception_time(self, start_date, offset, timezone):
        self.ensure_one()
        user_unavailable = []
        partner_exception = self.exception_ids
        if partner_exception:
            for my_appointment in partner_exception:
                # DATE START
                my_appointment_datetime = self.get_tz_date(datetime.strptime(str(my_appointment.start_datetime), DEFAULT_SERVER_DATETIME_FORMAT), timezone)
                exception_start_string = my_appointment_datetime.strftime(DEFAULT_SERVER_DATE_FORMAT)
                exception_start_date = datetime.strptime(exception_start_string, DEFAULT_SERVER_DATE_FORMAT)

                # DATE TO
                my_exception_to_datetime = self.get_tz_date(datetime.strptime(str(my_appointment.stop_datetime), DEFAULT_SERVER_DATETIME_FORMAT), timezone)
                exception_to_string = my_exception_to_datetime.strftime(DEFAULT_SERVER_DATE_FORMAT)
                exception_to_date = datetime.strptime(exception_to_string, DEFAULT_SERVER_DATE_FORMAT)
                # RANGE OF UNAVAILABLE DAYS
                exception_range = [(exception_start_date + timedelta(days=i)).strftime(DEFAULT_SERVER_DATE_FORMAT) for i in range(0, int(my_appointment.number_of_days_temp))]
                tody_date = start_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
                if tody_date in exception_range:
                    # MATCH WITH START DATE
                    if exception_start_string == tody_date:
                        total_min = self.string_to_minutes(my_appointment_datetime.strftime('%H:%M'))
                        start_tz_time = self.get_tz_date(my_appointment.start, timezone).replace(tzinfo=None)
                        end_tz_time = self.get_tz_date(my_appointment.stop, timezone).replace(tzinfo=None)
                        dims = my_appointment.stop - my_appointment.start
                        duration = dims.seconds/60
                        my_appointment_range = self.get_book_info_slots(start_tz_time, self.minutes_slot, duration)
                        user_unavailable = [a for a in my_appointment_range]
                    # MATCH WITH END DATE
                    elif exception_to_string == tody_date:
                        total_min = self.string_to_minutes(my_exception_to_datetime.strftime('%H:%M'))
                        start_tz_time = self.get_tz_date(my_appointment.start, timezone).replace(tzinfo=None)
                        end_tz_time = self.get_tz_date(my_appointment.stop, timezone).replace(tzinfo=None)
                        dims = my_appointment.stop - my_appointment.start
                        duration = dims.seconds/60
                        my_appointment_range = self.get_book_info_slots(start_tz_time, self.minutes_slot, duration)
                        user_unavailable = [a for a in my_appointment_range]
                    else:
                        start_tz_time = self.get_tz_date(my_appointment.start, timezone).replace(tzinfo=None)
                        end_tz_time = self.get_tz_date(my_appointment.stop, timezone).replace(tzinfo=None)
                        dims = my_appointment.stop - my_appointment.start
                        duration = dims.seconds/60
                        my_appointment_range = self.get_book_info_slots(start_tz_time, self.minutes_slot, duration)
                        user_unavailable = [a for a in my_appointment_range]
        return user_unavailable

    @api.constrains('minutes_slot', 'team_member')
    def check_minutes_slot(self):
        if self.team_member:
            if self.minutes_slot == 0 or self.minutes_slot < 0:
                raise ValidationError(_('please enter valid timeslot '))
