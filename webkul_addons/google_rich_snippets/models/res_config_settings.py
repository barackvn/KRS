# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################


from odoo import fields, models


class RichSnippetsConfig(models.TransientModel):
    _name = 'rich.snippets.config'
    _inherit = 'res.config.settings'

    is_organization_enable = fields.Boolean(
        string='Organization info',
        help="Organization related features like contact, logo & social profile.",
        config_parameter='google_rich_snippets.is_organization_enable')
    is_contact_enable = fields.Boolean(
        string='Corporate Contact',
        help="Your corporate contact information displayed in the Google Knowledge panel.",
        config_parameter='google_rich_snippets.is_contact_enable')
    is_logo_enable = fields.Boolean(
        string='Logo',
        help="Your organization's logo in search results and Google Knowledge Graph.",
        config_parameter='google_rich_snippets.is_logo_enable')
    is_social_enable = fields.Boolean(
        string='Social Profile',
        help="Your social profile information displayed on Google Knowledge panels.",
        config_parameter='google_rich_snippets.is_social_enable')

    is_website_enable = fields.Boolean(
        string='Website info',
        help="Website related features like Sitelinks Searchbox",
        config_parameter='google_rich_snippets.is_website_enable')
    is_searchbox_enable = fields.Boolean(
        string='Sitelinks Searchbox',
        help="A search box that is scoped to your website when it appears as a search result.",
        config_parameter='google_rich_snippets.is_searchbox_enable')

    is_carousels_enable = fields.Boolean(
        string='Carousels',
        help="Display your rich results in a sequential list or gallery in search results.",
        config_parameter='google_rich_snippets.is_carousels_enable')
    is_breadcrumb_enable = fields.Boolean(
        string='Breadcrumb',
        help="Navigation that indicates the page's position in the site hierarchy.",
        config_parameter='google_rich_snippets.is_breadcrumb_enable')
    is_rating_enable = fields.Boolean(
        string='Product Rating',
        help="The average rating based on multiple ratings or reviews of product.",
        config_parameter='google_rich_snippets.is_rating_enable')
    is_review_enable = fields.Boolean(
        string='Product Reviews',
        help="Public reviews posted on the product.",
        config_parameter='google_rich_snippets.is_review_enable')
    is_stock_enable = fields.Boolean(
        string='Product Availability',
        help="Display In Stock/Out of Stock based on Availability of the product.",
        config_parameter='google_rich_snippets.is_stock_enable')
