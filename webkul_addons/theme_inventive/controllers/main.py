# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import fields, http, tools
from odoo.http import request
from odoo.http import Controller

from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.mail import PortalChatter
import itertools
import os
import base64
import logging
_logger = logging.getLogger(__name__)

class InventiveWebsiteSale(WebsiteSale):
    @http.route()
    def save_shop_layout_mode(self, layout_mode):
        assert layout_mode in ('four_column_view', 'three_column_view', 'two_column_view', 'list_view'), "Invalid shop layout mode"
        request.session['website_sale_shop_layout_mode'] = layout_mode

    def _get_inventive_compute_currency(self):
        from_currency = self._get_pricelist_context()[1].currency_id
        to_currency = request.env.user.company_id.currency_id
        return lambda price: from_currency._convert(price, to_currency, (request.env.user).company_id, fields.Date.today())
    def _compute_currency(self):
            to_currency = self._get_pricelist_context()[1].currency_id
            from_currency = request.env.user.company_id.currency_id
            return lambda price: from_currency._convert(price, to_currency, (request.env.user).company_id, fields.Date.today())
    def _get_search_domain(self, search, category, attrib_values):
        domain = super(InventiveWebsiteSale, self)._get_search_domain(
            search=search, category=category, attrib_values=attrib_values)
        args = request.httprequest.args
        if bool(request.env['ir.config_parameter'].sudo().get_param('theme_inventive.show_price_filter')):
            min_price = args.get('min_price') and int(
                float(args.get('min_price'))) or False
            max_price = args.get('max_price') and int(
                float(args.get('max_price'))) or False
            if (min_price == 0 or min_price) and max_price:
                min_price = self._get_inventive_compute_currency()(min_price)
                max_price = self._get_inventive_compute_currency()(max_price)
                domain += [('list_price', '>=', min_price),
                           ("list_price", '<=', max_price)]
        # Product Tag Domain.................
        product_tag_ids = []
        for key,value in args.items():
            if "p_tag" in key:
                product_tag_ids.append(int(value))
        if product_tag_ids:
            domain += [('product_tag_id','in',product_tag_ids)]
        request.session['th_product_tag_ids'] = product_tag_ids
        return domain

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=12, **post):
        render = super(InventiveWebsiteSale, self).shop(
            page=page, category=category, search=search, ppg=ppg, **post)
        min_price = max_price = False
        keep = render.qcontext.get("keep", False)
        layout_mode = render.qcontext.get('layout_mode')
        if layout_mode=='list' or layout_mode == 'grid':
            layout_mode = layout_mode=='list' and 'list_view' or 'four_column_view'
        if keep:
            keep.args.update({
                'ppg': ppg,
                'min_price': post.get("min_price", False),
                'max_price': post.get("max_price", False)
            })
        render.qcontext.update({
            'ppg': ppg,
            'order': post.get("order", 'id'),
            "min_price": post.get("min_price", False),
            "max_price": post.get("max_price", False),
            "website_sale_shop_layout_mode":layout_mode,
            "compute_currency":self._compute_currency(),
            "layout_mode":layout_mode,
            "appyied_p_tags": request.session.get("th_product_tag_ids",[]),
        })

        if post.get("view") == "inventive-lazy-load":
            try:
                pager = render.qcontext.get("pager")
                if page <= pager.get("page_count"):
                    products = render.qcontext.get("products")
                    view = request.render(
                        "theme_inventive.inventive_lazy_list_product_item", render.qcontext)
                    return view
                else:
                    return False
            except Exception as e:
                _logger.info("\n++++++++++++++++++ERROR++++++%r+++++++++++++++++++++++++++", str(e))
        return render

    @http.route(['/inventive/product/extra/view/<model("product.template"):product>'], type='http', auth="public", website=True)
    def inventive_product_accessory_data(self, product, products_type, **kwargs):
        render = False
        template = ""
        if products_type == "alternative":
            product_ids = product.alternative_product_ids
            template = "theme_inventive.inventive_product_alternative_data_template"
        elif products_type == "accessories":
            product_ids = product.accessory_product_ids
            template = "theme_inventive.inventive_product_accessory_data_template"
        else:
            product_ids = False
        values = {
            'product': product,
            'product_ids': product_ids,
            'keep': QueryURL('/shop'),
            'slug': slug,
        }
        try:
            render = product_ids and request.render(template, values)
        except Exception as e:
            _logger.info(
                "\n++++++++++++++++++ERROR++++++%r+++++++++++++++++++++++++++", str(e))
        return render

    @http.route()
    def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        res = super(InventiveWebsiteSale, self).payment_validate(
            transaction_id=transaction_id, sale_order_id=sale_order_id, **post)
        location = ''
        for key, value in res.headers:
            if key == 'Location':
                location = value
        if location == '/shop/confirmation':
            return request.render("theme_inventive.inventive_congratulations_page", {'redirect': '/shop/confirmation'})
        else:
            return request.redirect('/shop')



class ThemeCustomerPortal(CustomerPortal):
    @http.route("/wk_image", type='json', auth="public", method='POST')
    def edit_image(self, **kw):
        res_user = request.env['res.users'].search(
            [('id', '=', request.env.user.id)])
        if kw.get('action') == 'edit':
            res_user.image = kw.get('data').split(',')[1].strip()
        else:
            for path in tools.config['addons_path'].split(','):
                try:
                    res_user.image = base64.b64encode(open(os.path.join(path, 'theme_inventive', 'static', 'src', 'img', 'unknown.png'), 'rb') .read()).decode("utf-8")
                except Exception as e:
                    _logger.info("..........Exception.......%r..................", str(e))

class AuthSignupHomeRedirect(AuthSignupHome):
    @http.route()
    def web_auth_signup(self, *args, **kw):
        kw.update({'redirect': "/inventive/thanks"})
        res = super(AuthSignupHomeRedirect, self).web_auth_signup(*args, **kw)
        return res

    @http.route('/inventive/thanks', type='http', auth='public', website=True, sitemap=False)
    def thankyou_page(self):
        return request.render("theme_inventive.inventive_thanks_page", {})

class ThemeSnippets(Controller):
    @http.route(['/snippet/featured-products/data/'], type="http", website=True, auth="public")
    def featured_products_data(self, name, type):
        render = False
        try:
            if name in ['featured-product', 'new-product', 'rated-product', 'popular-product']:
                references = request.website.get_keep_reference()
                website = request.website
                products = False
                method_name = 'get_inventive_%s_products' % name.split("-")[0]
                if hasattr(website, method_name):
                    products = getattr(website, method_name)()
                    values = {
                        'products': products,
                        'keep': references[0],
                        'slug': references[1],
                        'is_top_rated': name == 'rated-product',
                    }
                    if type and type == "2":
                        values["product_groups"] = list(itertools.zip_longest(*[iter(products)] * 3))
                        render = products and request.render(
                            "theme_inventive.inventive_featured_products_dynamic_2", values)
                    else:
                        render = products and request.render(
                            "theme_inventive.inventive_featured_products_dynamic_1", values)
                return render
            else:
                _logger.info(
                    "\n..........featured-products-name....%r ..not found...........", name)
        except Exception as e:
            _logger.info(
                "\n+++++++++ERROR++++++++++++++%r++++++++++++++++++++++", str(e))
        return render

    @http.route(['/snippet/products-tab/data/'], type="http", website=True, auth="public")
    def products_tab_data(self, name):
        render = False
        try:
            if name in ['all-products', 'latest-products', 'sale-products', 'best_seller-products']:
                references = request.website.get_keep_reference()
                website = request.website
                products = False
                method_name = 'get_inventive_%s_products' % name.split("-")[0]
                if hasattr(website, method_name):
                    products = getattr(website, method_name)()
                    values = {
                        'products': products,
                        'keep': references[0],
                        'slug': references[1],
                    }
                    render = products and request.render(
                        "theme_inventive.inventive_dynamic_tab_snippet_products", values)
        except Exception as e:
            _logger.info(
                "\n+++++++++ERROR++++++++++++++%r++++++++++++++++++++++", str(e))
        return render


class InventivePortalChatter(PortalChatter):
    @http.route()
    def portal_chatter_post(self, res_model, res_id, message, **kw):
        result = super(InventivePortalChatter, self).portal_chatter_post(res_model, res_id, message, **kw)
        if res_model == 'product.template' and kw.get('rating_value') and message:
            product = request.env['product.template'].sudo().browse(int(res_id))
            if product.exists():
                rating_value = float(kw.get('rating_value', 0))
                if product.product_avg_rating and rating_value:
                    increment = (rating_value - product.product_avg_rating) / (product.total_start_rating_count + 1)
                    product.product_avg_rating += increment
                    product.total_start_rating_count += 1
                else:
                    total = 0
                    rating = 0
                    for r_id in product.rating_ids:
                        if r_id.rating:
                            rating += r_id.rating
                            total += 1
                    product.total_start_rating_count = total
                    product.product_avg_rating = rating / total if total and rating else 0.0
        return result
class WebsiteBlog(http.Controller):
    @http.route(['/menu/dynamic'], type='http', auth='public', website=True)
    def render_latest_posts(self, template, category_id, domain=None, limit=None, order='published_date desc'):
        try:
            category = request.env['product.public.category'].search(
                [("id", '=', category_id)])
            param = {
                'keep': QueryURL('/shop/category/'),
                'slug': slug,
                'category': category,
            }
            render = request.render(template, param)
        except Exception as e:
            _logger.info("\n.....Exception .%r,.............", str(e))
        return render
