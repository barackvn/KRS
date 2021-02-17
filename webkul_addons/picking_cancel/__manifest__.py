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
    "name": "Odoo Stock Picking Cancel",
    "summary": "This module helps to cancel the done stock picking.",
    "category": "Warehouse",
    "version": "1.0.0",
    "sequence": 1,
    "author": "Webkul Software Pvt. Ltd.",
    "license": "Other proprietary",
    "website": "https://store.webkul.com/Odoo-Stock-Picking-Cancel.html",
    "description": """""",
    "live_test_url": "http://odoodemo.webkul.com/?module=picking_cancel",
    "depends": [
        'sale_stock',
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/picking_security.xml',
        'wizard/picking_cancel_wizard_view.xml',
        'views/picking_cancel_reason_view.xml',
        'views/picking_cancel.xml',
    ],
    "images": ['static/description/Banner.png'],
    "application": True,
    "installable": True,
    "auto_install": False,
    "price": 45,
    "currency": "EUR",
    "pre_init_hook": "pre_init_check",
}
