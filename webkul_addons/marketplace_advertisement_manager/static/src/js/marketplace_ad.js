/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('marketplace_advertisement_manager.marketplace_ad', function(require) {
    "use strict";
    var ajax = require('web.ajax');

    $(document).ready(function(){
        $('#select_ad_products_ids').selectpicker();

        $('[id^=adblockMultiple]').carousel({
          interval: 10000
        })

        $('[id^=adblockMultiple] .item').each(function(){
          var next = $(this).next();

          if (!next.length) {
            next = $(this).siblings(':first');
          }
          next.children(':first-child').clone().appendTo($(this));

          if (next.next().length>0) {
            next.next().children(':first-child').clone().appendTo($(this));
          }
          else {
            $(this).siblings(':first').children(':first-child').clone().appendTo($(this));
          }
        });

        if (document.getElementById("display_type_products") && document.getElementById("display_type_products").checked){
            $('#ad_block_products_content').css("display","block")
            $("#ad_block_banner_content").css("display","none")
            $("li.slider").find("a").addClass("active show")
        }
        else{
            $("#ad_block_banner_content").css("display","block")
            $('#ad_block_products_content').css("display","none")
            $("li.banner").find("a").addClass("active show")
        }

        $("li.banner").on("click", function(){
            $(document.getElementById("display_type_banner")).attr('checked', 'checked');
            $(document.getElementById("display_type_products")).removeAttr('checked');
            $("#ad_block_banner_content").css("display","block")
            $('#ad_block_products_content').css("display","none")
        })

        $("li.slider").on("click", function(){
            $(document.getElementById("display_type_products")).attr('checked','checked');
            $(document.getElementById("display_type_banner")).removeAttr('checked');
            $('#ad_block_products_content').css("display","block")
            $("#ad_block_banner_content").css("display","none")
        })

        $("#portal_add_products").on("click", function(){
            var block_id = parseInt($(this).data('block-id'))
            var max_products = parseInt($(this).data('max-products'))
            var ad_product_ids = []
            $('#select_ad_products_ids > option:selected').each(function() {
                if (this.value != ""){
                    ad_product_ids.push(parseInt(this.value))
                }
            });
            if (ad_product_ids.length <3){
                $("#show_req_prod_panel").css("display", "inline-block");
                $("#product_success_upd").css("display", "none");
                $("#show_rem_prod_panel").css("display", "none");
            }
            else if (ad_product_ids.length > max_products){
                $("#show_rem_prod_panel").css("display", "inline-block");
                $("#show_req_prod_panel").css("display", "none");
                $("#product_success_upd").css("display", "none");
            }
            else{
                $('.ad_loader').show();
                ajax.jsonRpc("/set/block/banner", "call", {
                    'block_id': block_id,
                    'ad_display_type': "ad_products",
                    'ad_product_ids': ad_product_ids,
                }).then(function(){
                    $("#product_success_upd").css("display", "inline-block");
                    $("#show_req_prod_panel").css("display", "none");
                    $("#show_rem_prod_panel").css("display", "none");
                    $('.ad_loader').hide();
                    location.reload(true);
                })
            }
        })

    });

});
