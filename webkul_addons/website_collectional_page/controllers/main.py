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

import werkzeug
from odoo import SUPERUSER_ID
from odoo import http
from odoo import tools
from odoo.http import request
from odoo.tools.translate import _
import math
from odoo.addons.website_sale.controllers.main import TableCompute, QueryURL
from odoo.osv import expression

import logging
_logger = logging.getLogger(__name__)

class WebsiteProduct(http.Controller):

    @http.route('/collections', type='http', auth="public", website=True)
    def get_all_collections(self, **post):
        collections_page = request.env['website.collectional.page'].sudo().search([('state','=','pub')])
        collections_group = request.env['website.collectional.group'].sudo().search([('state','=','published')])
        return request.render("website_collectional_page.website_collectional_page_n_groups",{
            'collections_page' : collections_page if collections_page else False,
            'collections_group': collections_group if collections_group else False,
        })

    def get_pricelist(self):
        return request.website.sudo().get_current_pricelist()

    @http.route([
        '/collections/<url_handler>', 
        '/collections/<url_handler>/page/<int:page>'
        ], type='http', auth="public", website=True)
    def get_collection(self, url_handler, page=0, category=None, search='', ppg=False, **post):
        
        def _get_search_domain(search):
            domains = [request.website.sudo().sale_product_domain()]
            domains.append([("id", "in", wk_collection.sudo().template_ids.ids)])

            if search:
                for srch in search.split(" "):
                    subdomains = [
                        [('name', 'ilike', srch)],
                        [('product_variant_ids.default_code', 'ilike', srch)],
                        [('description', 'ilike', srch)],
                        [('description_sale', 'ilike', srch)],
                    ]
                    domains.append(expression.OR(subdomains))
            
            domains = expression.AND(domains)
            
            product_obj = request.env['product.template'].sudo().search(domains)
            return request.env['product.template'].sudo().browse(product_obj.ids)

        uid, env , context = request.uid, request.env, dict(request.env.context)

        url = "/collections/" + str(url_handler)

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].sudo().get_current_website().shop_ppg or 20

        ppr = request.env['website'].sudo().get_current_website().shop_ppr or 4

        wk_collection = request.env['website.collectional.page'].sudo().search(
            [("url_handler", '=', url_handler)])

        if not context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            context['pricelist'] = int(pricelist)
        else:
            pricelist = env['product.pricelist'].sudo().browse(context['pricelist'])

        attrib_list = request.httprequest.args.getlist('attrib')
        keep = QueryURL(url, category=category and int(
            category), search=search, attrib=attrib_list)

        product_count = len(request.env["product.template"].sudo().search(
            [('sale_ok', '=', True), ("id", "in", wk_collection.sudo().template_ids.ids)]))
        pager = request.website.pager(
            url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        product_ids = request.env['product.template'].sudo().search([('sale_ok', '=', True), ('website_published','=',True),
            ("id", "in", wk_collection.sudo().template_ids.ids)], limit=ppg, offset=pager[
            'offset'], order='website_published desc, website_sequence desc')
        products = env['product.template'].sudo().browse(product_ids.ids)

        values = {
            'collectional_obj': wk_collection,
            'ppg': ppg,
            'ppr': ppr,
            'bins': TableCompute().process(products if not search else _get_search_domain(search), ppg, ppr),
            'products': products if not search else _get_search_domain(search),
            'hide_pager': len(_get_search_domain(search)),
            'pager': pager,
            "keep": keep,
            "pricelist": pricelist,
        }
        return request.render("website_collectional_page.wk_collection_product_view_website_sale", values)
