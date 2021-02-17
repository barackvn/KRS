/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

odoo.define("theme_inventive.header_default", function(require) {
    "use strict";
    var core = require('web.core');
    var _t = core._t;
    var ajax = require('web.ajax');
    var apply_overlay = require('theme_inventive.main_js')['apply_overlay'];
    var remove_overlay = require('theme_inventive.main_js')['remove_overlay'];
    var publicWidget = require('web.public.widget');
    publicWidget.registry.affixMenu = publicWidget.registry.affixMenu.extend({
        start: function() {
            if (this.editableMode) {
                return false;
            }
            this.th_navbar = this.$target.find("nav.navbar");
            this.th_header_top = this.$target.find(".inventive_header_top");
            // // Window Handlers
            $(window).on('resize.affixMenu scroll.affixMenu', _.throttle(this._onWindowUpdate.bind(this), 200));
            setTimeout(this._onWindowUpdate.bind(this), 0); // setTimeout to allow override with advanced stuff... see themes
            this._set_header();
            this.currentScroll = 0;
        },
        _onWindowUpdate: function() {
            var wOffset = $(window).scrollTop();
            var hOffset = this.$target.scrollTop();
            var self = this;
            if (wOffset > (hOffset + 100)) {
                this.th_navbar.addClass("slideUp");
                this.th_header_top.slideUp("slow");
                if (wOffset>this.currentScroll){
                    this.currentScroll = wOffset
                }else{
                    this.th_navbar.css("z-index","-1").removeClass("slideUp");
                    setTimeout(function(){
                        self.th_navbar.css("z-index","");
                    },500);
                    this.currentScroll = wOffset;
                }
            } else {
                this.th_navbar.css("z-index","-1").removeClass("slideUp");
                this.th_header_top.removeClass("slideUp");
                this.th_header_top.slideDown("slow");
                setTimeout(function(){
                    self.th_navbar.css("z-index","");
                },500);
            }
        },
        _set_header:function(){
            var header_affix = this.$target;
            this.$target.addClass("th_affixed");
            var main_nav = $('#oe_main_menu_navbar')
            var navbar = header_affix.find("nav.navbar");
            // main_nav.length !=0  ? header_affix.css("top",`${main_nav.offsetHeight-1}px`): header_affix.css("top","0px");
            var top_margin = `${header_affix.height() + navbar.height()}px`;
            $("#wrapwrap > main").css("margin-top",top_margin);
        },
    });
    publicWidget.registry.websiteSaleCartLink = publicWidget.Widget.extend({
        selector: '.th_cart_btn',
        read_events: {
            'click': '_onClickCartIcon',
            'click .js_delete_product': '_onClickDeleteProduct',
        },
        start: function() {
            var def = this._super.apply(this, arguments);
            if (this.editableMode) {
                return def;
            }
            this.main_nav = $('#oe_main_menu_navbar');
            return def;
        },
        _onClickCartIcon: function(ev) {
            var self = this;
            ev.preventDefault();
            ev.stopPropagation();
            var $slider = $("#th_mycart_slider");
            $slider.addClass("slide_left");
            apply_overlay();
            $("#wrapwrap").on('click','.overlay, #th_mycart_slider .close_icon',function(){
                remove_overlay();
                $slider.removeClass("slide_left");
            });
            if (this.main_nav.length !=0)
                $slider.css("top",this.main_nav.height() + "px");
            $.get("/shop/cart", {
                type: 'popover',
            }).then(function(data) {
                $slider.find(".dynamic_cart_content").html(data)
                $slider.on('click', '.js_delete_product', self._onClickDeleteProduct)
            });
        },
        _onClickDeleteProduct: function(ev) {
            var $th_cart_icon = $(".th_cart_btn");
            var $target = $(this).closest('.cart_line');
            var $input = $(this).closest('.cart_line').find('.js_quantity');
            $target.slideUp();
            ajax.jsonRpc("/shop/cart/update_json", 'call', {
                'line_id': parseInt($input.data('line-id'), 10),
                'product_id': parseInt($input.data('product-id'), 10),
                'set_qty': 0,
            }).then(function(data) {
                if (!data.cart_quantity)
                    $(".my_cart_quantity").html("0").hide().fadeIn(600);
                else
                    $(".my_cart_quantity").html(data.cart_quantity).hide().fadeIn(600);
                $.get("/shop/cart", {
                        'type': 'popover'
                    })
                    .then(function(data) {
                        $("#th_mycart_slider .dynamic_cart_content").html(data);
                        $("#th_mycart_slider .js_delete_product").bind('click', this._onClickDeleteProduct);
                    });
                let path = window.location.pathname;
                if (path.includes('/shop/cart')) {
                    window.location.href = path;
                }
            });
        },
    });

    $(document).ready(function() {
        const close_button = "<a class='btn btn-default btn-block dropdown-close'><i class='fa fa-long-arrow-left'/></a>"
        $("header").on('click', '.navbar-toggler', function(e) {
            e.preventDefault();
            e.stopPropagation();
            var btn = $(this);
            var menu = $("#top_menu_collapse");
            apply_overlay();
            $("#wrapwrap").on('click', '#top_menu_collapse .navbar-close,>.overlay', function(e) {
                var open_menu = menu.find(".o_mega_menu.show");
                if(open_menu.length===0){
                    remove_overlay();
                    menu.removeClass("slide_right");
                }
            })
            menu.addClass("slide_right").find("#top_menu").removeClass("text-right").find(".nav-item").addClass("w-100");
            var top = $("#oe_main_menu_navbar").length==1 ? "46px": "0px"
            menu.css("top", top);
        });
        $("#top_menu_collapse").on('click', '.inventive_mega_menu', function() {
            var link = $(this);
            var dropdown_menu = $(this).find(".dropdown-menu");
        });
    });
});
