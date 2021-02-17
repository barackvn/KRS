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
import odoo
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db
from odoo import http
from odoo.http import request
from odoo import tools
# from odoo.addons.web.controllers.main import binary_content
import base64
from odoo.tools.translate import _
from odoo import SUPERUSER_ID
# from odoo.addons.website.models.website import slug
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website_sale.controllers.main import TableCompute, QueryURL
from odoo.addons.web.controllers.main import Home
from odoo.addons.auth_signup.controllers.main import AuthSignupHome

from odoo.addons.website_mail.controllers.main import WebsiteMail
from odoo.addons.website_sale.controllers.main import WebsiteSale


from werkzeug import url_encode
import logging
_logger = logging.getLogger(__name__)



PPG = 20  # Products Per Page
PPR = 4   # Products Per Row

SPG = 20  # Shops Per Page
SPR = 4   # Shops Per Row




class WebsiteSale(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values):
        res = super(WebsiteSale, self)._get_search_domain(search, category, attrib_values)
        res.append(('wk_mp_membership', '=', False))
        return res

    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True):
        product_obj = request.env["product.product"].browse(product_id)
        if product_obj.wk_mp_membership:
            if set_qty:
                if set_qty > 1:
                    set_qty = 1
        return super(WebsiteSale, self).cart_update_json(product_id, line_id, add_qty, set_qty)

    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        sale_order_obj = request.website.sale_get_order()
        result = None
        if sale_order_obj and sale_order_obj.is_order_has_already_membership():
            add_qty = 0
        return super(WebsiteSale, self).cart_update(product_id, add_qty, set_qty)




class SellerMembership(http.Controller):

    @http.route(['/seller-membership-plan'], type='http', auth="public", website=True)
    def seller(self, seller_id=None, page=0, category=None, search='', ppg=False, **post):
        if not request.env.user.seller:
            return False
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        attributes_ids = set([v[0] for v in attrib_values])
        attrib_set = set([v[1] for v in attrib_values])

        domain = [('sale_ok', '=', True), ('wk_mp_membership', '=', True), ("website_published", "=", True)]


        keep = QueryURL('/shop', category=category and int(category), search=search, attrib=attrib_list, order=post.get('order'))
        pricelist_context = dict(request.env.context)
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        url = "/shop"
        if search:
            post["search"] = search
        if category:
            category = request.env['product.public.category'].browse(int(category))
            url = "/shop/category/%s" % slug(category)
        if attrib_list:
            post['attrib'] = attrib_list

        categs = request.env['product.public.category'].search([('parent_id', '=', False)])
        Product = request.env['product.template']

        parent_category_ids = []
        if category:
            parent_category_ids = [category.id]
            current_category = category
            while current_category.parent_id:
                parent_category_ids.append(current_category.parent_id.id)
                current_category = current_category.parent_id
        # Added by hasan to show only membership which is assigned by admin from seller crm start
        c_login_user=request.env['res.users'].browse(request.uid)
        product_count=0
        products=''
        if c_login_user:
            if c_login_user.partner_id.assign_membership:
                product_count=len(c_login_user.partner_id.assign_membership)
                products = c_login_user.partner_id.assign_membership
        # added End
        # below line comment by hasan to exclude to show all membership count
        # product_count = Product.search_count(domain)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        # below line comment by hasan to exclude to show all membership
        # products = Product.search(domain, limit=ppg, offset=pager['offset'])


        ProductAttribute = request.env['product.attribute']
        if products:
            attributes = ProductAttribute.search([('attribute_line_ids.product_tmpl_id', 'in', products.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg),
            'rows': PPR,
            'categories': categs,
            'attributes': attributes,
            'compute_currency': compute_currency,
            'keep': keep,
            'parent_category_ids': parent_category_ids,
        }
        if category:
            values['main_object'] = category
        return request.render("marketplace_membership.wk_mp_membership_plan", values)

    @http.route(['/view_membership_t_and_c'], type='json', auth="public", methods=['POST'], website=True)
    def view_membership_t_and_c(self, membership_product_id, **post):
        membership_product_obj = request.env["product.template"].browse(membership_product_id)
        return request.env.ref('marketplace_membership.wk_membership_product_t_and_c').render({
            'membership_product_obj': membership_product_obj,
        }, engine='ir.qweb')

    @http.route(['/check-membership-in-cart'], type='json', auth="public", methods=['POST'], website=True)
    def check_membership_already_in_cart(self, product_id, **post):
        membership_product_obj = request.env["product.product"].browse(int(product_id)) if product_id else None
        sale_order_id = request.session.get('sale_order_id')

        # Test validity of the sale_order_id
        sale_order = request.env['sale.order'].sudo().browse(sale_order_id) if sale_order_id else None
        membership_in_cart = sale_order.is_order_has_already_membership() if sale_order else None

        if (product_id and membership_in_cart and membership_in_cart == product_id) or (membership_product_obj.wk_mp_membership and membership_in_cart):
            return True
        return False
