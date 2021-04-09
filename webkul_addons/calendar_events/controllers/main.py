# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
from odoo import fields,api, http, tools, _
from odoo.http import request

import babel.dates
import re
import werkzeug
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.addons.website.controllers.main import QueryURL

# from odoo.addons.website.models.website import slug
from odoo.addons.http_routing.models.ir_http import slug

import logging
_logger = logging.getLogger(__name__)

class SellerWebsiteEventController(http.Controller):

    @http.route(['/event/calendar/day',], type='http', auth="public", website=True)
    def events(self, page=1, **searches):
        Event = request.env['event.event']
        EventType = request.env['event.type']
        searches.setdefault('search', '')
        searches.setdefault('date', 'cdate')
        searches.setdefault('type', 'all')
        searches.setdefault('country', 'all')

        c_date = searches.get('cdate')
        e_date = list(filter(lambda r: int(r) ,c_date.split('-')))
        sel_date = datetime(int(e_date[0]),int(e_date[1]),int(e_date[2]))
        c_date = sel_date.strftime('%m/%d/%Y')
        domain_search = {}

        def sdn(date):
            return fields.Datetime.to_string(date.replace(hour=23, minute=59, second=59))

        def sd(date):
            return fields.Datetime.to_string(date)

        today = datetime.today()
        dates = [
            ['cdate', _(c_date), [('date_begin','>',sd(sel_date)),('date_begin','<',sdn(sel_date))], 0],
            ['all', _('Next Events'), [("date_end", ">", sd(today))], 0],
            ['today', _('Today'), [
                ("date_end", ">", sd(today)),
                ("date_begin", "<", sdn(today))],
                0],
            ['week', _('This Week'), [
                ("date_end", ">=", sd(today + relativedelta(days=-today.weekday()))),
                ("date_begin", "<", sdn(today + relativedelta(days=6-today.weekday())))],
                0],
            ['nextweek', _('Next Week'), [
                ("date_end", ">=", sd(today + relativedelta(days=7-today.weekday()))),
                ("date_begin", "<", sdn(today + relativedelta(days=13-today.weekday())))],
                0],
            ['month', _('This month'), [
                ("date_end", ">=", sd(today.replace(day=1))),
                ("date_begin", "<", (today.replace(day=1) + relativedelta(months=1)).strftime('%Y-%m-%d 00:00:00'))],
                0],
            ['nextmonth', _('Next month'), [
                ("date_end", ">=", sd(today.replace(day=1) + relativedelta(months=1))),
                ("date_begin", "<", (today.replace(day=1) + relativedelta(months=2)).strftime('%Y-%m-%d 00:00:00'))],
                0],
            ['old', _('Old Events'), [
                ("date_end", "<", today.strftime('%Y-%m-%d 00:00:00'))],
                0],
        ]

        current_date = None
        current_type = None
        current_country = None
        for date in dates:
            if searches["date"] == date[0]:
                domain_search["date"] = date[2]
                if date[0] != 'all':
                    current_date = date[1]
        if searches["type"] != 'all':
            current_type = EventType.browse(int(searches['type']))
            domain_search["type"] = [("event_type_id", "=", int(searches["type"]))]

        if searches["country"] != 'all' and searches["country"] != 'online':
            current_country = request.env['res.country'].browse(int(searches['country']))
            domain_search["country"] = ['|', ("country_id", "=", int(searches["country"])), ("country_id", "=", False)]
        elif searches["country"] == 'online':
            domain_search["country"] = [("country_id", "=", False)]

        def dom_without(without):
            domain = [('state', "in", ['draft', 'confirm', 'done'])]
            for key, search in domain_search.items():
                if key != without:
                    domain += search
            return domain

        for date in dates:
            if date[0] != 'old':
                date[3] = Event.search_count(dom_without('date') + date[2])

        domain = dom_without('type')
        types = Event.read_group(domain, ["id", "event_type_id"], groupby=["event_type_id"], orderby="event_type_id")
        types.insert(0, {
            'event_type_id_count': sum([int(type['event_type_id_count']) for type in types]),
            'event_type_id': ("all", _("All Categories"))
        })

        domain = dom_without('country')
        countries = Event.read_group(domain, ["id", "country_id"], groupby="country_id", orderby="country_id")
        countries.insert(0, {
            'country_id_count': sum([int(country['country_id_count']) for country in countries]),
            'country_id': ("all", _("All Countries"))
        })

        step = 10
        event_count = Event.search_count(dom_without("none"))
        pager = request.website.pager(
            url="/event",
            url_args={'date': searches.get('date'), 'type': searches.get('type'), 'country': searches.get('country')},
            total=event_count,
            page=page,
            step=step,
            scope=5)

        order = 'website_published desc, date_begin'
        if searches.get('date', 'all') == 'old':
            order = 'website_published desc, date_begin desc'
        events = Event.search([('state','=','confirm'),('date_begin','>',sd(sel_date)),('date_begin','<',sdn(sel_date))], limit=step, offset=pager['offset'], order=order)

        keep = QueryURL('/event', **{key: value for key, value in searches.items() if (key == 'search' or value != 'all')})

        values = {
            'current_date': current_date,
            'current_country': current_country,
            'current_type': current_type,
            'event_ids': events,
            'dates': dates,
            'types': types,
            'countries': countries,
            'pager': pager,
            'searches': searches,
            'keep': keep,
        }
        return request.render("website_event.index", values)

class SellerEvents(http.Controller):

    @http.route(['/seller/event/list'], type='json', auth="public", methods=['POST'], website=True)
    def seller_event_list(self, **post):
        seller_event = request.env['event.event'].search([('state','=','confirm')])
        events = []
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        list1 = []
        for rec in seller_event:
            dic = {}
            name = rec.name
            title_name = name[:50]+'...' if len(name) > 50 else name
            event_url = base_url+"/event/%s" % slug(rec)
            date = rec.date_begin
            l1 = [date.year,date.month-1,date.day]
            if l1 not in list1:
                list1.append(l1)
                dic['date'] = l1
                dic['title'] = '<a href="'+event_url+'">'+title_name+'</a>'
                events.append(dic)
            else:
                for event in events:
                    if event['date'] == l1:
                        event['title'] = event['title']+'</br>'+'<a href="'+event_url+'">'+title_name+'</a>'
        return events
