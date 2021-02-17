/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

$(document).ready(function() {
	odoo.define('marketplace_membership.mp_membership', function (require)
    {
        "use strict";
        var core = require('web.core');
        var ajax = require('web.ajax');
	    var return_qty;
	    var _t = core._t;
		var temp = '1';
		$('.view_mship_t_and_c').on('click',function(e)		{
            var membership_product_id = parseInt($(this).find('.membership_product_id').first().val(),10);
			ajax.jsonRpc("/view_membership_t_and_c", 'call', {'membership_product_id': membership_product_id})
			.then(function (vals)
			{
                var $modal = $(vals);
	            $modal.appendTo('#wrap')
                .modal('show')
                .on('hidden.bs.modal', function () {
                    $(this).remove();
                });
	        });
		});

		$('.oe_website_sale').each(function() {
            var oe_website_sale = this;

            $(oe_website_sale).on("change", ".oe_cart input.js_quantity", function(ev) {

                var $input = $(this);
                var value = parseInt($input.val(), 10);
                var $dom = $(this).closest('tr');
                var line_id = parseInt($input.data('line-id'), 10);
                var product_id = parseInt($input.data('product-id'), 10);
                if (value > 1)
                {
	                ajax.jsonRpc("/check-membership-in-cart", 'call', {
	                    'product_id': parseInt($input.data('product-id'), 10),
	                })
	                .then(function(result) {
	                    if (result) {
	                        $dom.popover('dispose');
	                        $dom.popover({
	                            content: _t("You can purchase only 1 quantity of membership."),
	                            title: _t("WARNING"),
	                            placement: "top",
	                            trigger: 'focus',
	                            timeout : 1000000,
	                        });
	                        $dom.popover('show');
	                        setTimeout(function() {
	                            $dom.popover('dispose')
	                        }, 5000);
	                        ev.preventDefault();
	                        ev.stopPropagation();
	                    } else {
	                        $dom.popover('dispose');
	                    }
	                });
	            }
            });
            // function for '/shop/product' page product quantity vailidation on click of add to cart button
            $(oe_website_sale).on("click", '#add_to_cart', function(ev) {
                var $form = $(this).closest('form');
                if ($("input[name='product_id']").is(':radio'))
                    var product_id = $("input[name='product_id']:checked").attr('value');
                else
                    var product_id = $("input[name='product_id']").attr('value');
                var add_qty = parseFloat($form.find('input[type="text"][name="add_qty"]').first().val(), 10);
                ajax.jsonRpc("/check-membership-in-cart", 'call', {
                    'product_id': product_id,
                })
                .then(function(result) {
                    if (result) {
                    	ev.preventDefault();
                        ev.stopPropagation();
                        $form.find('input[type="text"][name="add_qty"]').first().val(temp);
                        $('#add_to_cart').popover({
                            content: _t("You can purchase only 1 membership item with only 1 quantity."),
                            title: _t("WARNING"),
                            placement: "left",
                            trigger: 'focus',
                        });
                        $('#add_to_cart').popover('show');
                        setTimeout(function() {
                            $('#add_to_cart').popover('dispose')
                        }, 2000);
                    } else {
                        $('#add_to_cart').popover('dispose');
                        temp = add_qty.toString();
                    }
                });
            });

            // function for '/shop/product' page product quantity vailidation on increment of product quantity
            $(oe_website_sale).find('input[type="text"][name="add_qty"]').on('change', function(ev) {
                var $form = $(this).closest('form');
                if ($("input[name='product_id']").is(':radio'))
                    var product_id = $("input[name='product_id']:checked").attr('value');
                else
                    var product_id = $("input[name='product_id']").attr('value');
                var add_qty = parseFloat($form.find('input[type="text"][name="add_qty"]').first().val(), 10);
                if (add_qty > 1)
                ajax.jsonRpc("/check-membership-in-cart", 'call', {
                    'product_id': product_id,
                })
                .then(function(result) {
                    if (result) {
                        $form.find('input[type="text"][name="add_qty"]').first().val(temp);
                        $('.css_quantity').popover({
                            content: _t("You can purchase only 1 quantity of membership."),
                            title: _t("WARNING"),
                            placement: "top",
                            trigger: 'focus',
                        });
                        $('.css_quantity').popover('show');
                        setTimeout(function() {
                            $('.css_quantity').popover('dispose');
                        }, 2000);
                    } else {
                        $('.css_quantity').popover('dispose');
                        temp = add_qty.toString();
                    }
                });
            });

            // Commenting this method because same functionality is used in the method below this method

            // $(oe_website_sale).on('click', 'a.btn.btn-default.btn-xs', function(ev) {
            //     var $form = $(this).closest('form');
            //     var $msg = $form.find('.fa-shopping-cart');
            //     var product_id = parseInt($form.find('input[type="hidden"][name="product_id"]').first().val(), 10);
            //     ajax.jsonRpc("/check-membership-in-cart", 'call', {
            //         'product_id': product_id,
            //     })
            //     .then(function(result) {
            //         if (result) {
            //             $(this).addClass('disabled');
            //             alert(_t("You can add only one membership product with 1 quantity in to cart."))
            //         }
            //     });
            // });

			$(document).on("click", ".wk_panel-footer a.a-submit", function (ev)
			{
				ev.stopPropagation();
    			ev.stopImmediatePropagation();
				var $form = $(this).closest('form');
                var $msg = $form.find('.fa-shopping-cart');
                var product_id = parseInt($form.find('input[type="hidden"][name="product_id"]').first().val(), 10);
                ajax.jsonRpc("/check-membership-in-cart", 'call', {
                    'product_id': product_id,
                })
                .then(function(result) {
                    if (result) {
                        $(this).addClass('disabled');
                        alert(_t("You can add only one membership product with 1 quantity in to cart."))
                    }
                });
			});
        });
	});
});
