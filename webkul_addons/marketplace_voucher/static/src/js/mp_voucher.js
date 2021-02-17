/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('marketplace_voucher.mp_voucher', function (require) {
    "use strict";

    var base = require('web_editor.base');
    var core = require('web.core');
    var ajax = require('web.ajax');

    $(document).ready(function(){
        $('.oe_website_sale').on("change", ".oe_cart input.js_quantity", function(ev){
            var $input = $(this);
            var value = parseInt($(this).val() || 0, 10)
            var line_id = parseInt($input.data('line-id'),10)
            var product_id = parseInt($input.data('product-id'), 10)

            ajax.jsonRpc("/shop/cart/update_cart_voucher", "call", {
                'product_id':product_id,
                'line_id':line_id,
                'set_qty':value,
            }).then(function(line){
                // location.reload();
                console.log("====",line)
            })
        })
    });
});
