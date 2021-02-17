/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define('odoo_stock_per_warehouse.WebsiteSale', function (require) {
    'use strict';

    var core = require('web.core');
    var sAnimations = require('website.content.snippets.animation');

    sAnimations.registry.WebsiteSale = sAnimations.registry.WebsiteSale.extend({
        xmlDependencies: [
            '/odoo_stock_per_warehouse/static/src/xml/stock_available_info.xml'
        ],
        _onChangeCombination: function(ev, $parent, values) {
            console.log(values.show_stocks)
            if (values.show_stocks)
            {
                console.log(values.show_qty)
                $('.stock_available_info').html(
                    $(core.qweb.render('StockAvailableInfo', {
                            warehouse_stocks: values.warehouse_stocks,
                            show_qty        : values.show_qty,
                        })
                    )
                )
                this._super(this, $parent, values);
            }
        }
    });
});

