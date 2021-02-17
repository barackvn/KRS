/* Copyright (c) 2020-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

odoo.define('theme_marketplace_inventive.shop_page', function(require) {
    'use strict';
    var sAnimations = require('website.content.snippets.animation');

    sAnimations.registry.shopProductHoverEffect = sAnimations.Class.extend({
        selector:'.inmp_seller_shop',
        events:{
            "click .nav-item .nav-link":"_onClickNavLink"
        },
        start:function(){
            this._super.apply(this,arguments);
        },
        _onClickNavLink:function(ev){
            var self = this;
            var currentTarget = $(ev.currentTarget);
            var tabContent = currentTarget.parents(".container");
            var hashUrl = currentTarget.attr('href');
            this.target = tabContent.find(hashUrl);
            Promise.race([
                this.executer(1000),
                this.executer(2000),
                this.executer(3000),
                this.executer(4000),
            ]).then((res)=>{
                self.hover_effect_on_products();
            }).catch((err)=>{
                console.log("errpr in promiss == ",err);
            });
        },
        executer:function(time){
            var self = this;
            return new Promise(function(resolve,reject){
                setTimeout(()=>{
                    if(self.target.find(".four_column_view").length>0){
                        resolve();
                    }
                },time)
            })
        },
        hover_effect_on_products:function(){
            $(".four_column_view .oe_product,.three_column_view .oe_product,.two_column_view .oe_product ").each(function() {
                var image = $(this).find(".oe_product_image");
                var buttons = $(this).find("section .product_price > .btn-secondary");
                var btn_cart_height = $(this).find("section .product_price > .btn-cart").height();
                var count = buttons.length;
                var btn_width = buttons.first().width();
                var margin  = (image.width() - btn_width*count - 20*(count-1))/2;
                var top = -(btn_cart_height + buttons.first().height() + 10)
                var loop_count = 0;
                var value = 0;
                buttons.each(function() {
                    value += loop_count == 0 ? margin : btn_width + 20;
                    $(this).css("right", value).css("top",top).css("transition-delay", (.1 * loop_count) + "s");
                    loop_count += 1;
                });
                var quick_view_btn = $(this).find("section .product_price > .inventive_product_quick_view");
                quick_view_btn.css("top",-(image.height()/2 + quick_view_btn.height()/2 + btn_cart_height/2 ) ).css("right",(image.width()/2 - quick_view_btn.width()/2 -10 ))
            });
            $(".two_column_view .oe_product").each(function() {
                var subdescription = $(this).find(".oe_subdescription");
                if(subdescription.height()>=50){
                    subdescription.addClass("gradient");
                }
            });
        }
    });
});
