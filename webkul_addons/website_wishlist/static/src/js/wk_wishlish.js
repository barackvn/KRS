odoo.define('website_wishlist.website_wishlist', function(require) {
    "use strict";
    var ids;
    var ajax = require('web.ajax');
    var base = require('web_editor.base');
    var core = require('web.core');
    var utils = require('web.utils');
    var publicWidget = require('web.public.widget');
    var _t = core._t;



    $(document).ready(function() {
        
        var last_product=false;
        $('.oe_website_sale').each(function(ev) {
            var oe_website_sale = this;
            check_wishlist_onload();
            $(oe_website_sale).on('change', function(ev) {
                var product_id = check_product_id();
                if ($.inArray(product_id, ids) != -1) {
                    added_to_wishlist();
                } else {
                    add_to_wishlist();
                }
            });

            $(oe_website_sale).on('click', 'a.add_to_wishlist', function(ev) {
                var product = check_product_id();
                ajax.jsonRpc('/wishlist/add_to_wishlist', 'call', {
                    'product': product,
                })
                .then(function(res) {
                    if (res > 0) {
                        ids.push(product.toString());
                        $('.my_wishlist_quantity').parent().parent().removeClass("hidden");
                        $('.my_wishlist_quantity').html(res).hide().fadeIn(600);
                    } else {
                        $('.my_wishlist_quantity').parent().parent().addClass("hidden");
                    }
                });
                added_to_wishlist();
            });

            $(oe_website_sale).on("click", "a.remove_whishlist", function(ev) {
                last_product = $(this).attr("last");
                var product_id = $(this).attr("whishlist-id");
                var row = $(this).closest('tr');
                remove_wishlist_product(product_id, row);
            });

            function price_to_str(price) {
                
                var l10n = _t.database.parameters;
                var precision = 2;

                if ($(".decimal_precision").length) {
                    precision = parseInt($(".decimal_precision").last().data('precision'));
                }
                var formatted = _.str.sprintf('%.' + precision + 'f', price).split('.');
                formatted[0] = utils.insert_thousand_seps(formatted[0]);
                return formatted.join(l10n.decimal_point);
            }

            function update_product_image(event_source, product_id) {
                var $img = $(event_source).closest('.wk_wishlist_row').find("img");
                var $cart_btn = $(event_source).closest('.wk_wishlist_row').find("#wishlist_to_cart");
                $img.parent().attr('data-oe-model', 'product.product').attr('data-oe-id', product_id)
                    .data('oe-model', 'product.product').data('oe-id', product_id);
                $cart_btn.attr("product-id", product_id);
                $img.attr("src", "/web/image/product.product/" + product_id + "/image_small");
            }
            
            $(oe_website_sale).on("click", "a#wishlist_to_cart", function(ev) {
                var row = $(this).closest('tr');
                var product_id = parseInt(row.find('.product_id').val(), 10);
                last_product = $(this).attr("last");
                var value = 1;
                var $input = $(this);
                if ($input.data('update_change')) {
                    return;
                }
                ajax.jsonRpc("/shop/cart/update_json", 'call', {
                    'line_id': NaN,
                    'product_id': product_id,
                    'add_qty': value
                })
                .then(function(data) {
                    remove_wishlist_product(product_id, row);
                    $input.data('update_change', false);
                    if (value !== 1) {
                        $input.trigger('change');
                        return;
                    }
                    var $q = $("li#my_cart");
                    if (data.cart_quantity) {
                        $q.removeClass("d-none");
                    } else {
                        // $q.addClass("d-none");
                        $('a[href^="/shop/checkout"]').addClass("hidden")
                    }
                    $q.find(".my_cart_quantity").html(data.cart_quantity).hide().fadeIn(600);
                });
            });

            function remove_wishlist_product(product_id, row) {
                ajax.jsonRpc('/wishlist/remove_from_wishlist', 'call', {
                    'product': product_id,
                })
                .then(function(res) {
                    if (res >= 0 ) {
                        $('.my_wishlist_quantity').parent().parent().removeClass("hidden");
                        $('.my_wishlist_quantity').html(res).hide().fadeIn(600);
                    } else {
                        $('.my_wishlist_quantity').parent().parent().addClass("hidden");
                    }
                    if (last_product)
                        window.location.reload();
                });
                row.fadeOut(1000);

            }

            function check_wishlist_onload() {
                ids = $('#wishlist_ids').attr('ids');
                if (ids)
                    ids = ids.replace(/[\[\]']+/g, '').replace(/\s/g, '').split(',');
                else
                    ids = [];
                var product_id = check_product_id();
                if (product_id === '0') {
                    $("div.wishlist-box").hide();
                }
                if ($.inArray(product_id, ids) != -1) {
                    added_to_wishlist();
                } else {
                    add_to_wishlist();
                }
            }

            function check_product_id() {
                if ($("input[name='product_id']").is(':radio'))
                    var product_id = $("input[name='product_id']:checked").attr('value');
                else
                    var product_id = $("input[name='product_id']").attr('value');
                if (product_id === '0') {
                    $("div.wishlist-box").hide();
                } else {
                    $("div.wishlist-box").show();
                }
                return product_id
            }

            function added_to_wishlist() {
                $(".add_to_wishlist").html('Added to Wishlist');
                $(".add_to_wishlist").addClass('wishlist_disabled');
                $(".add_to_wishlist").parent().css("color","#990000");
            }

            function add_to_wishlist() {
                $(".add_to_wishlist").html(' Add to Wishlist');
                $(".add_to_wishlist").removeClass('wishlist_disabled');
                $(".add_to_wishlist").parent().css("color","black");
            }
        });
    });
});
