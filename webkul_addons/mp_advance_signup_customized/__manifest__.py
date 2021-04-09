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
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
    'name': 'Marketplace advance signup customized',
    'version': '1.0.0',
    'description': """
        res partner speciality field
        exclusively for you menu on website
    
    """,
    'summary': 'Marketplace advance signup customized for res partner',
    'author': 'Webkul Software Pvt. Ltd.',
    'website': 'store.webkul.com',
    'license': 'Other proprietary',
    'category': 'website',
    'depends': [
        'odoo_marketplace',
        'advance_signup'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/speciality_views.xml',
        'views/views_inherit.xml'
    ],
    'auto_install': False,
    'application': True,
    'pre_init_hook': 'pre_init_check',
}