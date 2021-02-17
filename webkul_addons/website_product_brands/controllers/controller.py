# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# License URL : <https://store.webkul.com/license.html/>
#################################################################################
import werkzeug
from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.http_routing.models.ir_http import slug
from odoo.http import request

class WebsiteSale(WebsiteSale):
    @http.route(
        ['''/shop''',
         '''/shop/page/<int:page>''',
         '''/shop/category/<model("product.public.category"):category>''',
         '''/shop/category/<model("product.public.category"):category>/page/<int:page>''',
         '''/shop/brand/<model("wk.product.brand"):wk_brand>''',
          '''/shop/brand/<model("wk.product.brand"):wk_brand>/page/<int:page>'''],
        type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, wk_brand=None,  **post):
        response= super(WebsiteSale, self).shop(page=page, category=category,
        search=search, ppg=ppg, **post
        )

        brand =(post.get('brand')  and post.get('brand')) or False
        attrib_brands = request.httprequest.args.getlist('attrib_brand')
        brand_set=[]
        for attrib_brand in attrib_brands:
            attrib_brand_index = attrib_brand.split('-')[0]
            if brand:
                if (brand!=attrib_brand_index):
                    brand_set+=[int(attrib_brand_index)]
            else:
                brand_set+=[int(attrib_brand_index)]
        response.qcontext['brand_set']= list(set(brand_set))
        response.qcontext['brand_rec']= request.env['wk.product.brand'].search([('website_published','=',True)])
        response.qcontext['wk_brands']= request.env['wk.product.brand'].browse(list(set(brand_set)))

        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = request.env['website'].get_current_website().shop_ppg or 20

        ppr = request.env['website'].get_current_website().shop_ppr or 4

        qcontext = dict(response.qcontext)
        attrib_list = request.httprequest.args.getlist('attrib')
        url = "/shop"
        if search:
            post["search"] = search
        if category:
            category = request.env['product.public.category'].browse(int(category))
            url = "/shop/category/%s" % slug(category)
        if attrib_list:
            post['attrib'] = attrib_list
        search_count = len(qcontext.get('products'))
        pager = request.website.pager(url=url, total=qcontext.get('search_count'),
        page=page, step=ppg, scope=7, url_args=post)
        response.qcontext['pager'] = pager
        keep = QueryURL('/shop', category=category and int(category), search=search,
        attrib=attrib_list, order=post.get('order'),attrib_brand=attrib_brands)
        response.qcontext['keep'] = keep
        return response

    def _get_search_domain(self, search, category, attrib_values):
        domain= super(WebsiteSale, self)._get_search_domain(search, category, attrib_values)
        domain = self._get_brand_domain(domain,search, category, attrib_values)

        return domain
    def _get_brand_domain(self,domain,search, category, attrib_values):
        attrib_brands = request.httprequest.args.getlist('attrib_brand')
        brand = request.httprequest.args.getlist('brand')
        brand_set=[]
        for attrib_brand in attrib_brands:
            attrib_brand_index = attrib_brand.split('-')[0]
            if brand:
                if brand[0]!=attrib_brand_index:
                    brand_set+=[int(attrib_brand_index)]
            else:
                brand_set+=[int(attrib_brand_index)]
        if len(brand_set):
            domain += [('product_brand_id.id', 'in', list(brand_set))]

        return domain

    def _get_brand(self, products):
        product_brands = []
        [product_brands.append(product.product_brand_id) for product in products if len(
            product.product_brand_id) and product.product_brand_id not in product_brands]
        return product_brands
