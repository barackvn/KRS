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

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class PortalAccount(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(PortalAccount, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        fav_sellers_count = request.env['marketplace.seller.followers'].search_count([
            ('customer_id', '=', partner.id),
        ])
        values['fav_sellers_count'] = fav_sellers_count
        return values

    @http.route(['/my/favourite/sellers', '/my/favourite/sellers/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_favourite_sellers(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        FavSeller = request.env['marketplace.seller.followers']

        domain = [
            ('customer_id', '=', partner.id),
        ]

        searchbar_sortings = {
            'create_date': {'label': _('Create Date'), 'order': 'create_date desc'},
        }
        # default sort by order
        if not sortby:
            sortby = 'create_date'
        order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('marketplace.seller.followers', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        fav_sellers_count = FavSeller.search_count(domain)

        # make pager
        pager = request.website.pager(
            url="/my/favourite/sellers",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=fav_sellers_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        fav_sellers = FavSeller.search(domain, limit=self._items_per_page, offset=pager['offset'], order=order)
        values.update({
            'date': date_begin,
            'fav_sellers': fav_sellers,
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/favourite/sellers',
            'page_name': 'favourite_seller',
            'sortby': sortby,
        })
        if kw.get('add_favourite_success'):
            values.update({
                'add_favourite_success' : kw.get('add_favourite_success'),
            })
        if kw.get('add_favourite_error'):
            values.update({
                'add_favourite_error' : kw.get('add_favourite_error'),
            })
        if kw.get('seller_remove_success'):
            values.update({
                'seller_remove_success' : kw.get('seller_remove_success'),
            })
        return request.render("marketplace_favourite_seller.portal_my_favourite_sellers_list", values)
