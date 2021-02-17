/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

odoo.define("theme_inventive.main_js", function(require) {
    "use strict";
    var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');
    $(document).ready(function(){
        $('#holdon-overlay').slideUp(600);
        $('#holdon-content-container').fadeOut(300);

        // .........Home Page carousel snippet .............
        var $target = $(".s_inventive_owl_carousel_snippet .owl-carousel");
        if ($target.length>0){
            $target.removeAttr("data-animateIn").removeAttr("data-animateOut");
            $.each($target.prev().data(), function( key, value ){
                $target.attr('data-' + key,value);
            });
            inventive_owl_carousel($target);
        }
        // .........th_related_products carousel snippet .............
        $target = $("#th_related_products .owl-carouse");
        // My Account Page js............................................................
        $('#wrap.o_portal_wrap').on('click','.delete_icon',function(){
            ajax.jsonRpc('/wk_image','call',{'action':'delete'}).then(function(){
                location.reload();
            });
        });
        $('#wrap.o_portal_wrap').on('click','#apply_image',function(){
            var file = document.querySelector('#file').files[0];
            var reader  = new FileReader();
            reader.addEventListener("load", function () {
                var result = reader.result;
                ajax.jsonRpc('/wk_image', 'call', {
                    'action': 'edit',
                    'data': result
                }).then(function(){
                    location.reload();
                });
            }, false);
            if(file){
                reader.readAsDataURL(file);
            }
        });
    });
    // ..........Scroll To top....................
    publicWidget.registry.inventive_scroll_to_top = publicWidget.Widget.extend({
        selector:'#th_scroll_to_top_btn',
        read_events:{
            'click':'_scroll_to_top'
        },
        start:function(ev){
            $(window).on('scroll', _.throttle(this._onWindowUpdate.bind(this), 200));
            this.$target = $(this.selector);
        },
        _onWindowUpdate: function (ev) {
            var wOffset = $(window).scrollTop();
            this.$target.toggleClass('animate', wOffset > 300);
        },
        _scroll_to_top:function(){
            $('html,body').animate({ scrollTop: 0 }, 1000);
        }
    });
    // ....................OWL CAROUSEL .........................................
    let carouselDefaultOptions = {
        lazyLoad:true,
        autoplayHoverPause:true,
        autoWidth:false,
        navText:["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],

    }
    let carouselResponsiveOptions = {
        responsive:{
            0:{
                items:1
                },
            480:{
                items:1
            },
            768 : {
                items:1
            },
            991 : {
                items:1
            }
        }
    }
    function inventive_owl_carousel($target,responsive=false){
        var options = new Object();
        if( $target){
            options.items                   = $target.data("items") ||  1;
            options.loop                    = true && $target.data("loop");
            options.rewind                  = true && $target.data("rewind") || false;
            options.dots                    = $target.data("dots") || false;
            options.autoWidth               = true && $target.data("autowidth") || true;
            options.nav                     = true && $target.data("nav") || false;
            options.slideBy                 = $target.data("slideBy") || 1;
            options.autoplay                = $target.data("autoplay") || false;
            options.autoplayTimeout         = $target.data("autoplayTimeout") || $target.data("autoplaytimeout") || 3000;
            options.autoplaySpeed           = $target.data("autoplaySpeed") || $target.data("autoplayspeed") || 2000;
            options.smartSpeed              = $target.data("smartSpeed") || $target.data("smartspeed") || 1000;
            options.center                  = $target.data("center") || false;
            options.animateIn               = $target.data("animateIn") || $target.data("animatein") || false;
            options.animateOut              = $target.data("animateOut") || $target.data("animateout") || false;
            options.dotsEach                = $target.data("dotsEach") || $target.data("dotseach") || false;
            options.stagePadding            = $target.data("stagePadding") || $target.data("stagepadding") || 0;
            Object.assign(options, carouselDefaultOptions);
            if (responsive){
                Object.assign(options, carouselResponsiveOptions);
                options.responsive[0].items     = $target.data('small-items') || $target.data('smallitems') || 1;
                options.responsive[480].items   = $target.data('mobile-items') || $target.data('mobileitems') || 1;
                options.responsive[768].items   = $target.data('tab-items') || $target.data('tabitems') || 1;
                options.responsive[991].items   = $target.data('desktop-items') || $target.data('desktopitems') || 1;
            }
            $target.owlCarousel(options);
        }else{
            console.log("Theme Inventive says Target Object Is Not Defined");
        }
    };
    var affix_header;
    var main_top_margin;
    function apply_overlay(ev){
        affix_header = $("header.o_affix_enabled");
        main_top_margin = $("main").css("margin-top");
        var body = $("body");
        $("#wrapwrap").addClass("apply_overlay");
        body.css('overflow', "hidden");
        if ($(window).innerWidth() > 1200) {
            body.css("padding-right", "10px");
        }
        if (affix_header.length != 0) {
            affix_header.removeClass("o_affix_enabled");
            $("main").css("margin-top", '');
        }
    };
    function remove_overlay() {
        $("#wrapwrap").removeClass("apply_overlay");
        $("body").css('overflow', "").css("padding-right", "");
        if (affix_header && affix_header.length != 0) {
            affix_header.addClass("o_affix_enabled");
            $("main").css("margin-top", main_top_margin);
        }
    }
    function apply_scrollbar(element){
      if(element){
        window.Scrollbar.init(element);
      }
    }
    return {
        "owl_carousel":inventive_owl_carousel,
        "apply_overlay":apply_overlay,
        "remove_overlay":remove_overlay,
        "th_scrollbar": apply_scrollbar,
        }
});
