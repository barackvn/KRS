##########################################################################
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
##########################################################################
{
    'name'         : 'Stock Per Warehouse',
    'summary'      : 'Show Stock available for the products per Warehouse',
    'description'  : '''
Odoo Stock Balance by Location
Odoo Stocks Location
product Stock
Odoo Warehouse management and Routing
Inventory Per Stock
Display Stock Per Warehouse
Show stock in Odoo website
Display stock by warehouse on product page
odoo Product Warehouse Quantity
Product Warehouse Quantity
Odoo Product Warehouse Capacity
    ''',
    'category'     : 'Warehouse',
    'version'      : '1.0.02',

    'author'       : 'Webkul Software Pvt. Ltd.',
    'website'      : 'https://store.webkul.com/Odoo.html',
    'license'      : 'Other proprietary',
    'live_test_url': 'http://odoodemo.webkul.com/?module=odoo_stock_per_warehouse&custom_url=/shop/product/customizable-desk-9',

    'depends'      : [
        'website_sale_stock',
        'website_webkul_addons'
    ],
    'data'          : [
        'security/ir.model.access.csv',

        'views/product_template.xml',
        'views/product_product.xml',
        'views/warehouse_stock_config.xml',
        'views/website_webkul_addons.xml',
        'wizard/warehouse_stock_visibilty_update.xml',
        'templates/web.xml',

        'data/warehouse_stock_configs.xml',
    ],
    'images'        : [
        'static/description/banner.png'
    ],

    'sequence'     : 1,
    'application'  : True,
    'installable'  : True,
    'pre_init_hook': 'pre_init_check',
    "price"        : 35,
    'currency'     : 'EUR',
}
