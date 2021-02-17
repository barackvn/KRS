odoo.define('theme_inventive.snippets_js', function(require) {
  'use strict';

  var core = require('web.core');
  var _t = core._t;

  var publicWidget = require('web.public.widget');
  var owl_carousel = require('theme_inventive.main_js')['owl_carousel'];
  var ProductQuickViews = require("theme_inventive.shop_page_js")['productQuickViews']
  const s_demo_product = "<div class='s_product dummy_view'>\
                                <div class='s_product_image'>\
                                    <i class='fa fa-file-image-o'/>\
                                </div>\
                                <div class='s_product_content'>\
                                    <h5></h5>\
                                    <span class='inventive_product_price'>\
                                    </span>\
                                    <div class='inventive_product_rating_star'>\
                                        <div class='o_website_rating_static'>\
                                            <i class='fa fa-star-o'></i>\
                                            <i class='fa fa-star-o'></i>\
                                            <i class='fa fa-star-o'></i>\
                                            <i class='fa fa-star-o'></i>\
                                            <i class='fa fa-star-o'></i>\
                                            <span class='rating_val'> / 0 </span>\
                                        </div>\
                                    </div>\
                                </div>\
                            </div>"
  const dummy_tab_product = "<div class='oe_product oe_product_cart dummy_view'>\
                                    <form action='/shop/cart/update' method='post'>\
                                        <div itemscope='itemscope' itemtype='http://schema.org/Product'>\
                                            <div class='oe_product_image'>\
                                                <div><i class='fa fa-picture-o'/></div>\
                                            </div>\
                                            <section>\
                                                <h6/>\
                                                <span class='inventive_product_price'/>\
                                                <div class='inventive_product_rating_star'>\
                                                    <div class='o_website_rating_static'>\
                                                        <i class='fa fa-star-o'></i>\
                                                        <i class='fa fa-star-o'></i>\
                                                        <i class='fa fa-star-o'></i>\
                                                        <i class='fa fa-star-o'></i>\
                                                        <i class='fa fa-star-o'></i>\
                                                        <span class='rating_val'> / 0 </span>\
                                                    </div>\
                                                </div>\
                                            </section>\
                                        </div>\
                                    </form>\
                                </div>"
  publicWidget.registry.s_FeaturedProducts = publicWidget.Widget.extend({
    selector: '.s_inventive_featured_products_1 , .s_inventive_featured_products_2',
    start: function() {
      var self = this;
      var $snippet = this.$target;
      var type = parseInt($snippet.data('type'))
      $snippet.find(".s_dynamic_data").each(function() {
        var name = $(this).data('name');
        var $dynamic_div = $(this);
        if (type == 1) {
          $dynamic_div.empty();
          var i;
          for (i = 0; i < 5; i++) {
            $dynamic_div.append(s_demo_product);
          }
        } else {
          $dynamic_div.html("<div class='data_loader' data-loader='wave'></div>")
        }
        if (name && !$("body").hasClass("editor_enable")) {
          $.get("/snippet/featured-products/data/", {
            'name': name,
            'type': type
          }, function() {}).then(function(data) {
            if (data) {
              $dynamic_div.append(data);
              if (type == 2) {
                $dynamic_div.attr({
                  "data-loop": false,
                  "data-nav": true
                });
                $dynamic_div.find(".data_loader").remove();
                owl_carousel($dynamic_div);
                $dynamic_div.find(".owl-nav").hide();
                var nav = $dynamic_div.parent().find(".f_product_nav");
                nav.find(".owl-next").click(function() {
                  $dynamic_div.trigger('next.owl.carousel')
                  $(this).attr('class', $dynamic_div.find(".owl-next").attr("class"))
                  nav.find(".owl-prev").attr('class', $dynamic_div.find(".owl-prev").attr("class"))
                });
                nav.find(".owl-prev").click(function() {
                  $dynamic_div.trigger('prev.owl.carousel')
                  $(this).attr('class', $dynamic_div.find(".owl-prev").attr("class"))
                  nav.find(".owl-next").attr('class', $dynamic_div.find(".owl-next").attr("class"))
                });
                if ($dynamic_div.find("owl-item") && $dynamic_div.find(".owl-item").length < 2)
                  nav.addClass("disabled");
              } else {
                $dynamic_div.addClass("fade_out_dummy_view");
                setTimeout(function() {
                  $dynamic_div.find(".dummy_view").remove();
                  $dynamic_div.find(".dyn_products").css("z-index", "10").css('position', 'static');
                  $dynamic_div.removeClass("fade_out_dummy");
                }, 1300);
              }
            }
          });
        } else {
          $dynamic_div.removeClass("fade_out_dummy_view");
        }
      });
    },
  });
  publicWidget.registry.s_FeaturedProductsTabs = publicWidget.Widget.extend(new ProductQuickViews, {
    selector: '.s_inventive_product_nav_tabs_1,.s_inventive_product_nav_tabs_2',
    start: function() {
      var self = this;
      var $snippet = this.$target;
      var type = parseInt($snippet.data('type'))
      $snippet.find(".s_dynamic_data").each(function() {
        var $dynamic_div = $(this);
        var name = $dynamic_div.data('name');
        var i;
        $dynamic_div.empty();
        if (type == 1) {
          for (i = 0; i < 4; i++) {
            $dynamic_div.append(dummy_tab_product);
          }
        }
        if (name && !$("body").hasClass("editor_enable")) {
          $.get("/snippet/products-tab/data/", {
            'name': name
          }, function() {}).then(function(data) {
            if (data) {
              $dynamic_div.append(data)
              $dynamic_div.find(".oe_product.dummy_view").remove();
              var $dyn_products = $dynamic_div.find(".dyn_products");
              $dyn_products.addClass("owl-carousel owl-theme");
              $dyn_products.owlCarousel({
                  autoplayHoverPause:true,
                  autoplay:true,
                  navText:["<i class='fa fa-angle-left'></i>","<i class='fa fa-angle-right'></i>"],
                  loop:true,
                  nav:true,
                  dots:false,
                  autoplayTimeout:3000,
                  center:true,
                  smartSpeed:1000,
                  responsive:{
                      0:{
                          items:1
                          },
                      480:{
                          items:1
                      },
                      768 : {
                          items:3
                      },
                      991 : {
                          items:4
                      }
                  }
              });
              var nav = $snippet.find(".f_product_nav");
            }
          });
        }
      });
    },
  });
});
