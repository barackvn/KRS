/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define("theme_inventive.product_page_js", function(require) {
    "use strict";
    var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');
    var owl_carousel = require('theme_inventive.main_js')['owl_carousel'];
    var th_scrollbar = require('theme_inventive.main_js')['th_scrollbar'];
    var ProductQuickViews = require("theme_inventive.shop_page_js")['productQuickViews']
    $(document).ready(function() {
        //......Replacing the rating.............................
        var $source_rating = $("#wrap .o_shop_discussion_rating");
        var $target_rating = $("#wrap .o_shop_inventive_discussion_rating")
        var $source_detail = $("#product_full_spec");
        var $target_detail = $("#inventive_p_full_spec");
        if ($source_rating.length>0){
            $target_rating.replaceWith($source_rating);
            $("#p_review_tab").removeClass("d-none");
        }
        if($source_detail.length>0){
            $source_detail.removeClass("d-none");
            $target_detail.replaceWith($source_detail);
            $("#p_detail_tab").removeClass("d-none");
        }
        $('#product_details .rating_count a').on('click', function (e) {
          $('#inventive_product_tabs .nav-tabs a[href="#wk_product_review"]').tab('show');
        });
    });
    publicWidget.registry.WebsiteSale = publicWidget.registry.WebsiteSale.extend({
        read_events: _.extend({
            "click .carousel-indicators li": "_activeCarouselImage",
            "click .tigger" : "_tiggerVariantChange",
            "click .carousel-control-next": "_nextItem",
            "click .carousel-control-prev": "_prevItem",
        }, publicWidget.registry.WebsiteSale.prototype.read_events),
        start:function(){
        		var def = this._super.apply(this, arguments);
                if (this.editableMode) {
        		    return def;
        		}
            this._alternativeProductsOwlCarousel();
            this._replace_quantity();
            th_scrollbar(document.querySelector('#product_details .th_product_desc p'));
            return def;
        },
        _updateProductImage: function ($productContainer, productId, productTemplateId, new_carousel){
            this._super.apply(this, arguments);
            this._offer_timer();
            this.$carouselIndicators = $productContainer.find("#o-carousel-product .carousel-indicators");
            this.$carousel = $productContainer.find("#o-carousel-product");
            var $li = this.$carouselIndicators.find("li");
            var totalWidth = ($li.width()+10)*$li.length;
            var $el = $("#inventive_product_item_view_modal .modal-content");
            var count=0;
            this.$carousel.addClass("animated");
            this.$carouselIndicators.removeClass("position-static text-left")
            if(this.$el.hasClass("modal-content")){
                this.$carouselIndicators.addClass("vertical");
                var width = 370;
                var left =  ($el.width()/2)-(width/2)-30
                var item_count = parseInt(width/($li.width()+1))
                this.$carouselIndicators.css({"width":width+'px',"left":left+'px',});
                if( totalWidth>width){
                    this.$carouselIndicators.attr({
                      "data-tabitems":item_count,
                      "data-desktopitems":item_count,
                      "data-nav":  true,
                      "data-smartspeed":500,
                    });
                    owl_carousel(this.$carouselIndicators,true);
                }
            }else{
                var item_count = parseInt(this.$carouselIndicators.width()/($li.width()+10))
                if( totalWidth>this.$carouselIndicators.width()){
                    this.$carouselIndicators.attr({
                      "data-tabitems":item_count,
                      "data-desktopitems":item_count,
                      "data-mobileitems":4,
                      "data-smallitems":3,
                      "data-nav": true,
                      "data-smartspeed":500,
                    });
                    owl_carousel(this.$carouselIndicators,true);
                }
            }
        },
        _tiggerVariantChange:function(ev){
            this.triggerVariantChange(this.$el);
        },
        _offer_timer:function(ev){
          var end_date= this.$el.find("input[name='end_date']").val();
          if(end_date != undefined){
              $(this.$el).find(".deal_countdown_timer").countdown({
                date: end_date,
                offset: +0,
                day: 'day',
                days: 'day',
                hour:   'hrs',
                hours: 'hrs',
                minute: 'min',
                minutes:'min',
                seconds:'sec',
                second:'sec',
              },
              function () {
                window.loaction.reload();
              }
            );
          }
        },
        _nextItem: function(ev) {
            var carousel_obj =this.$carousel.find(".carousel-inner div.active").next();
            var carousel = carousel_obj.length != 0 ? carousel_obj.attr("value") :  this.$carousel.find(".carousel-inner>div").attr("value");
            var li = this.$carouselIndicators.find(`li[value=${carousel}]`);
              li.addClass("active",10);
              $('.carousel-indicators').trigger('to.owl.carousel', parseInt(li.attr("data-slide-to")));
        },
        _prevItem: function(ev) {
          var carousel_obj =this.$carousel.find(".carousel-inner div.active").prev();
          var carousel = carousel_obj.length != 0 ? carousel_obj.attr("value") :  this.$carousel.find(".carousel-inner>div:last-child").attr("value");
          var li = this.$carouselIndicators.find(`li[value=${carousel}]`);
            li.addClass("active",10);
            $('.carousel-indicators').trigger('to.owl.carousel', parseInt(li.attr("data-slide-to")));
        },
        _activeCarouselImage:function(ev){
            $(ev.target).closest("li").addClass("active", 10);
        },
        _onChangeCombination:function(ev, $parent, combination){
            this._super.apply(this, arguments);
            var target = $('#product_details .inventive_product_price .product_price')
            var source = $('#product_details .js_product .product_price ')
            target.html(source.html());
        },
        _alternativeProductsOwlCarousel:function(ev){
            var $target = this.$target.find(".alternative_products .column");
            var items = parseInt($target.data("items"),10);
            $target.each(function(){
                if($(this).find(".owl-carousel").length!=0){
                    var $owl_carousel = $(this).find(".owl-carousel");
                    $owl_carousel.owlCarousel({
                      autoplayHoverPause:true,
                      autoplay:true,
                      navText:["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
                      loop:false,
                      nav:true,
                      dots:false,
                      autoplayTimeout:3000,
                      smartSpeed:1000,
                      responsive:{
                          0:{
                              items:1
                              },
                          480:{
                              items:2
                          },
                          768 : {
                              items:3
                          },
                          991 : {
                              items:4
                          }
                      }
                    })
                    var nav = $owl_carousel.find(".owl-nav");
                    if($owl_carousel.find(".owl-nav").hasClass("disabled")){
                        $(this).find(".owl-next,.owl-prev").addClass("disabled");
                    }else{
                        nav.hide();
                        $(this).find(".owl-next").click(function() {
                            $owl_carousel.trigger('next.owl.carousel');
                            $(this).parent().find(".owl-prev").removeClass("disabled");
                            $owl_carousel.find(".owl-next.disabled").length!=0?$(this).addClass("disabled"):$(this).removeClass("disabled");
                        });
                        $(this).find(".owl-prev").click(function() {
                            $owl_carousel.trigger('prev.owl.carousel');
                            $(this).parent().find(".owl-next").removeClass("disabled");
                            $owl_carousel.find(".owl-prev.disabled").length!=0?$(this).addClass("disabled"):$(this).removeClass("disabled");
                        }).addClass("disabled");
                    }
                }
            })
        },
        _replace_quantity:function(ev){
            var $qty = $("#product_details .js_product .css_quantity");
            var $add_to_cart_btn = $("#product_details .js_product .add_to_cart_btn");
            $qty.detach().appendTo($add_to_cart_btn);
        }
    });
    publicWidget.registry.productAlternateProducts = publicWidget.Widget.extend(new ProductQuickViews,{
        selector:"#product_detail > .alternative_products",
    });
});
