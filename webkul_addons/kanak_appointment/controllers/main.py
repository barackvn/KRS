# -*- coding: utf-8 -*-
import pytz
import uuid

from datetime import datetime, timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from odoo import fields, http
from odoo.http import request


class KanakAppointment(http.Controller):

    _days_per_page = 7
    _total_days = 30
    _day_diff = 0

    @http.route('/team', auth="public", website=True)
    def team_list(self, **post):
        partners = request.env['res.partner'].sudo().search([('team_member', '=', True)])
        return request.render('kanak_appointment.kanak_select_partner', {'partners': partners})

    def get_booking_date(self, times="0:0", date=None):
        booking_times = times.split(":")
        booking_time = int(booking_times[0]) * 60 + int(booking_times[1])
        return datetime.strptime(str(date), '%d/%m/%Y') + timedelta(minutes=booking_time)

    def check_next_day(self, available=[], times=[], partner=None):
        Partner = request.env['res.partner']
        time_min = Partner.string_to_minutes(times)
        res = []
        for avail in available:
            avail_min = Partner.string_to_minutes(avail)
            if avail_min > time_min:
                nex_avail_min = avail_min - 1440
                res.append(Partner.minutes_to_string(nex_avail_min))
        return res

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

    def value_to_string_html(self, value):
        hours, minutes = divmod(abs(value) * 60, 60)
        minutes = round(minutes)
        if minutes == 60:
            minutes = 0
            hours += 1
        if value < 0:
            return '-%02d:%02d' % (hours, minutes)
        return '%02d:%02d' % (hours, minutes)

    def get_utc_date(self, date=None, timezone=None):
            to_zone = pytz.timezone('UTC')
            from_zone = pytz.timezone(timezone)
            return from_zone.localize(date).astimezone(to_zone)

    def get_tz_date(self, date=None, timezone=None):
        to_zone = pytz.timezone(timezone)
        from_zone = pytz.timezone('UTC')
        return from_zone.localize(date).astimezone(to_zone)

    @http.route(['/member/appointment/<int:partner_id>',
                 '/member/appointment/<int:partner_id>/page/<int:page>',
                 '/appointment/reschedule/<int:partner_id>'
                 ], auth="public", website=True, csrf=False)
    def appointment_member(self, partner_id=None, page=1, token=None, tz=None, **post):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        date_format = "%m/%d/%Y"

        browser_timezone = post.get('timezone')
        if browser_timezone:
            request.session['timezone'] = browser_timezone
        req_tz = pytz.timezone(request.session.get('timezone', 'UTC'))
        user_tz = pytz.timezone(partner.tz)
        offset = (req_tz.utcoffset(datetime.now()).total_seconds() - user_tz.utcoffset(datetime.now()).total_seconds()) / 3600
        cal_start_date = datetime.strptime(str(datetime.now().strftime(date_format)), date_format)
        lunch_start = float(partner.lunch_start) * 60
        lunch_end = float(partner.lunch_end) * 60
        # If min and max date are set calendar start from min date and end on max date
        if partner.min_date and partner.max_date:
            self._total_days = 1 + (fields.Datetime.from_string(partner.max_date) - fields.Datetime.from_string(partner.min_date)).days
            cal_start_date = fields.Datetime.from_string(partner.min_date)
            minutes_offset = 100 - (float(("%.2f" % offset).split('.')[1]) + float(("%.2f" % partner.exraoffset).split('.')[1]))
            time_offset = partner.get_minutes(minutes_offset)
            times = [a for a in partner.get_range(float(minutes_offset) / 60.0, (1440 - time_offset) / 60.0, (float(partner.minutes_slot) / 60))]
            if post.get('jump_date'):
                jump_date = datetime.strptime(str(post.get('jump_date')), date_format)
                self._day_diff = (cal_start_date - jump_date).days
                self._total_days += self._day_diff
                cal_start_date = jump_date

            pager = request.website.pager(
                url='/member/appointment/%s' % (partner_id),
                total=self._total_days,
                page=page,
                step=self._days_per_page,
            )
            day_slot = (page - 1) * self._days_per_page
            break_time = next_day_available = dates = []
            for i in range(0, self._total_days):
                start_date = cal_start_date + timedelta(days=i)
                dayname = start_date.strftime('%a')
                available = next_day_available
                if partner[dayname.lower()]:
                    offset_min = offset * 60
                    # USER TIMEZONE TIME BREAK
                    new_start_date = start_date.date()
                    lunch_start_time = self.value_to_string_html(partner.lunch_start)
                    lunch_end_time = self.value_to_string_html(partner.lunch_end)
                    break_time = self.get_daily_slots(start=lunch_start_time, end=lunch_end_time, slot=partner.minutes_slot, date=new_start_date, partner=partner, timezone=request.session.get('timezone', 'UTC'))
                    break_time = break_time + partner.get_booked_time(start_date, offset_min, request.session.get('timezone', 'UTC'))

                    # Dont Display Time if user is on Holidays
                    break_time = break_time + partner.get_exception_time(start_date, offset, request.session.get('timezone', 'UTC'))
                    new_start_time = self.value_to_string_html(partner['%s_from' % dayname.lower()])
                    new_end_time = self.value_to_string_html(partner['%s_to' % dayname.lower()])
                    
                    new_times = self.get_daily_slots(start=new_start_time, end=new_end_time, slot=partner.minutes_slot, date=new_start_date, partner=partner, timezone=request.session.get('timezone', 'UTC'))
                    available_range = new_times
                    # available_range = partner.get_range((p_from + offset_min) / 60, (to + offset_min) / 60, (float(partner.minutes_slot) / 60))
                    available = [a for a in available_range if a not in break_time] + next_day_available

                    dates.append([dayname, start_date.strftime('%d/%m/%Y'), available])
                    next_day_available = list(set(self.check_next_day(available, times[-1:][0], partner)) - set(break_time))
            partner_available_time = [date[2] for date in dates]
            max_range = sorted(set([item for sublist in partner_available_time for item in sublist]))
            values = {
                'partner': partner,
                'dates': dates[day_slot:(day_slot+self._days_per_page)],
                'times': times,
                'set_timezone': request.session.get('timezone'),
                'pager': pager,
                'max_range': max_range,
                'partner_available_time': partner_available_time,
                'appointment_available': self._day_diff <= 0,
                'jump_date': post.get('jump_date'),
                'appointment': '',
                'msg': ''
            }
            if token:
                appointment = request.env['calendar.attendee'].sudo().search([('access_token', '=', token)])
                pager = request.website.pager(
                    url='/appointment/reschedule/%s?token=%s' % (partner_id, token),
                    total=self._total_days,
                    page=page,
                    step=self._days_per_page,
                )
                values.update({'appointment': appointment, 'set_timezone': appointment.partner_id.tz, 'pager': pager})
                if datetime.strptime(str(appointment.event_id.app_date), "%Y-%m-%d %H:%M:%S") < datetime.now():
                    values['msg'] = 'Thank You. No action was taken as that booking is in the past.'
            return request.render('kanak_appointment.kanak_member_calendar', values)

    @http.route('/member/book/<int:partner_id>', auth="public", website=True)
    def book_member(self, partner_id=None, **post):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        times = post.get('time') and post.get('time').split(':') or [0, 0]
        metting_time = int(times[0]) * 60 + int(times[1])
        date = datetime.strptime(str(post.get('date')), '%d/%m/%Y') + timedelta(minutes=metting_time)
        post['booking'] = date.strftime('%A, %B %d, %Y %H:%M')
        post['partner'] = partner
        post['req_partner'] = request.env.user.partner_id if not request.env.user._is_public() else None
        return request.render('kanak_appointment.kanak_member_book', post)

    @http.route('/confirm/booking/<int:partner_id>', auth="public", website=True)
    def booking_confirm(self, partner_id=None, **post):
        Partner = request.env['res.partner'].sudo()
        appointment_with = Partner.sudo().browse(partner_id)
        date = self.get_booking_date(post.get('time', "00:00"), post.get("date"))
        utc_date = Partner.get_utc_date(date, post.get('timezone'))
        date_appointment = str(date.strftime('%A, %B %d, %Y %H:%M'))
        partner = Partner.search([('email', '=', post.get('email'))], limit=1)
        if not partner:
            partner = Partner.sudo().create({
                'name': "%s %s" % (post.get('first_name'), post.get('last_name') and post.get('last_name') or ''),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'tz': post.get('timezone'),
            })
        if partner:
            if not partner.tz:
                partner.sudo().tz = post.get('timezone')

        user_id = request.env['res.users'].sudo().search([('partner_id', '=', appointment_with.id)], limit=1)
        if not user_id:
            user_id = request.env.ref('base.user_admin').sudo()
        event = {
            'name': '%s-%s' % (post.get('first_name'), fields.Datetime.to_string(date)),
            'app_date': fields.Datetime.to_string(utc_date),
            'app_partner_id': appointment_with.id,
            'app_time': str(utc_date.strftime('%H:%M')),
            'date_appointment': date_appointment,
            'app_duration': str(timedelta(minutes=int(appointment_with.minutes_slot)))[0:4],
            'partner_ids': [(6, 0, [appointment_with.id , partner.id])],
            'start': fields.Datetime.to_string(utc_date),
            'stop': fields.Datetime.to_string((utc_date + timedelta(minutes=int(appointment_with.minutes_slot)))),
            'start_datetime': fields.Datetime.to_string(utc_date),
            'stop_datetime': fields.Datetime.to_string((utc_date + timedelta(minutes=int(appointment_with.minutes_slot)))),
            'end_date_time': fields.Datetime.to_string((utc_date + timedelta(minutes=int(appointment_with.minutes_slot)))),
            'meet_flag': True,
            'type': 'appointment',
            'user_id': user_id.id
        }
        app = request.env['calendar.event'].sudo().with_context(no_mail_to_attendees=True).create(event)
        template = request.env.ref('kanak_appointment.kanak_calendar_booking')
        for attendee in app.attendee_ids:
            template.sudo().send_mail(attendee.sudo().id, force_send=True)

        post['date'] = date_appointment
        return request.render('kanak_appointment.appointment_thankyou', post)

    @http.route('/appointment/reschedule/pre_conformation/<int:partner_id>/<string:access_token>', auth="public", website=True)
    def booking_reschedule(self, partner_id=None, access_token=None, **post):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        appointment = request.env['calendar.attendee'].sudo().search([('access_token', '=', access_token)])
        date = self.get_booking_date(post.get('time', "00:00"), post.get("date"))
        date_appointment = str(date.strftime('%A, %B %d, %Y %H:%M'))
        post.update({'appointment': appointment, 'partner': partner, 'date_appointment': date_appointment})
        return request.render('kanak_appointment.appointment_reschedule', post)

    @http.route('/confirm/reschedule/<int:partner_id>/<string:access_token>', auth="public", website=True)
    def reschedule_confirm(self, partner_id=None, access_token=None, **post):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        appointment = request.env['calendar.attendee'].sudo().search([('access_token', '=', access_token)])
        date = self.get_booking_date(post.get('time', "00:00"), post.get("date"))
        utc_date = partner.get_utc_date(date, post.get('timezone'))
        date_appointment = str(date.strftime('%A, %B %d, %Y %H:%M'))
        appointment.event_id.sudo().write({
            'name': '%s-%s' % (appointment.partner_id.name, fields.Datetime.to_string(date)),
            'app_date': fields.Datetime.to_string(utc_date),
            'app_time': str(utc_date.strftime('%H:%M')),
            'date_appointment': date_appointment,
            'start': fields.Datetime.to_string(utc_date),
            'stop': fields.Datetime.to_string((utc_date + timedelta(minutes=int(partner.minutes_slot)))),
            'start_datetime': fields.Datetime.to_string(utc_date),
            'stop_datetime': fields.Datetime.to_string((utc_date + timedelta(minutes=int(partner.minutes_slot)))),
        })
        post.update({'date': date_appointment})
        return request.render('kanak_appointment.appointment_thankyou', post)

    @http.route('/appointment/cancel/<int:partner_id>', auth="public", website=True)
    def booking_cancel(self, partner_id=None, token=None, **post):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        appointment = request.env['calendar.attendee'].sudo().search([('access_token', '=', token)])
        post.update({'appointment': appointment, 'partner': partner, 'date_appointment': appointment.event_id.date_appointment})
        return request.render('kanak_appointment.appointment_cancel', post)

    @http.route('/confirm/cancel/<int:partner_id>/<string:access_token>', auth="public", website=True)
    def confirm_cancel(self, partner_id=None, access_token=None, **post):
        appointment = request.env['calendar.attendee'].sudo().search([('access_token', '=', access_token)])
        appointment.event_id.app_state = 'cancel'
        return request.render('kanak_appointment.appointment_cancel_thankyou')
