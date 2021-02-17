odoo.define('theme_inventive.shop_page_js', function(require) {
    'use strict';

    var ajax = require('web.ajax');
    var wSaleUtils = require('website_sale.utils');
    var publicWidget = require('web.public.widget');
    var WebsiteSale = publicWidget.registry.WebsiteSale;
    var main_js = require('theme_inventive.main_js');
    var owl_carousel = main_js['owl_carousel'];
    var apply_overlay = main_js['apply_overlay'];
    var remove_overlay = main_js['remove_overlay'];
    var th_scrollbar = main_js['th_scrollbar'];
    var WebsiteSaleLayout = publicWidget.registry.WebsiteSaleLayout
    var WebsiteSaleOptions = publicWidget.registry.WebsiteSaleOptions

    //  Products Layout Views..........................................
    publicWidget.registry.WebsiteSaleLayout = WebsiteSaleLayout.extend({
        disabledInEditableMode: false,
        events: {
            'click .shift_shop_view': '_onApplyShopLayoutChange',
        },
        _onApplyShopLayoutChange: function(ev) {
            var $target = $(ev.currentTarget);
            var switchToLayout = $target.data('class');
            if (!this.editableMode) {
                this._rpc({
                    route: '/shop/save_shop_layout_mode',
                    params: {
                        'layout_mode': switchToLayout ? switchToLayout : 'four_column_view',
                    },
                });
            }
            $target.parent().find(".shift_shop_view").removeClass("active");
            $target.addClass("active")
            var $grid = $('#products_grid');
            $grid.removeClass('four_column_view').removeClass('three_column_view').removeClass('two_column_view').removeClass('list_view');
            $grid.addClass(switchToLayout);
        },

    });
    publicWidget.registry.productGridHeader = publicWidget.Widget.extend({
        selector: '.products_grid_header',
        events: {
            'click .remove_attribute_filter': '_onClickRemoveFilter',
        },
        start: function() {
            $('#products_grid .remove_attribute_filter').hover(function() {
                $(this).parents(".active-filter").addClass("active");
            }, function() {
                $(this).parents(".active-filter").removeClass("active");
            });
        },
        _onClickRemoveFilter:function(ev){
            var $target = $(ev.currentTarget);
            var attr = $target.data("attr");
            if (attr) {
                $target.parents(".active-filter").addClass("disabled");
                var href = this._removeSubString(attr, window.location.href);
                var attr_categ = $target.data("categ");
                if (attr_categ) {
                    href = this._removeSubString(attr, href)
                }
                window.location = href;
            }
        },
        _removeSubString:function(subStr, sourceURL){
            var new_str = "&" + subStr;
            var href = sourceURL.indexOf(new_str) != -1 ? sourceURL.replace(new_str, '') : sourceURL.replace(subStr, '')
            return href
        },

    });

    // Inventive Category Filter Button................................
    publicWidget.registry.categoryFilters = publicWidget.Widget.extend({
        selector: '.inventive_categ_filters',
        events: {
            'click .btn': '_onClick',
        },
        init: function() {
            this._super.apply(this, arguments);
            this.$products_grid_before = $("#products_grid_before");
            this.$parent = $(".inventive_shop_page");
            this.$products_grid = $("#products_grid");
            this.mode = this.$parent.data('filters-mode');
        },
        start: function() {
            var mode = this.mode;
            if (mode == "side_bar" || window.window.innerWidth < 1200) {
                this.$products_grid_before.removeClass("col-lg-3").addClass("slide_left slider");
                this.$products_grid.find(".th_products_pager").css("position", "relative");
                this.$products_grid_before.detach().appendTo(this.$parent);
                var self = this;
                $("#wrapwrap").on('click', '.overlay, #products_grid_before .navbar-close', function() {
                    self._remove_overlay();
                });
            } else if (mode == "dropdown") {
                this.$products_grid_before.removeClass("col-lg-3").addClass("shutter_down shutter");
                this.$products_grid.find(".th_products_pager").css("position", "relative");
                this.$products_grid.find(".th_products_pager").append("<div class='product_filter_div w-100' style='display:none'/>");
                this.$product_filter_div = this.$products_grid.find(".product_filter_div");

                this.$products_grid_before.detach().appendTo(this.$product_filter_div);
                this.$product_filter_div.slideUp(1);
                var self = this;
                $("#wrapwrap").on('click', '#wrap', function() {
                    self.$product_filter_div.slideUp("slow");
                    $(this).find('.inventive_categ_filters >.btn').removeClass("active");
                });
                th_scrollbar(document.querySelector('#products_grid_before .in_product_attributes'));
                th_scrollbar(document.querySelector('#wsale_products_categories_collapse'));

            } else {
                $(".o_wsale_products_main_row").css("margin-left", "0px");
                this.$products_grid_before.addClass("default")
                this.$el.addClass("d-none");

            }
            this.$products_grid_before.removeClass("d-none");
            document.querySelectorAll('#wsale_products_attributes_collapse .nav-pills .collapse').forEach(element=>{
              th_scrollbar(element);
            });
            return this._super.apply(this, arguments);
        },
        _onClick: function(ev) {
            ev.stopPropagation();
            if (this.mode == "side_bar" ||  window.window.innerWidth < 1200) {
                this.$products_grid_before.addClass("slide_right").removeClass("slide_left");
                this._apply_overlay();
            }
            else if (this.mode == "dropdown") {
                this.$product_filter_div.slideToggle("slow");
                $(ev.currentTarget).toggleClass("active");
            }
            else {}
        },
        _apply_overlay: function(ev) {
            apply_overlay();
        },
        _remove_overlay: function() {
            this.$products_grid_before.removeClass("slide_right").addClass("slide_left");
            remove_overlay();
        }
    });
    // price Filter js
    publicWidget.registry.inventivePriceFilter = publicWidget.Widget.extend({
        selector: '.inventive_price_range_filter',
        events: {
            'change .range-slider': '_onChangePriceRange',
        },
        init: function() {
            this._super.apply(this, arguments);
        },
        start: function() {
            var $price_range = this.$el.find('input.range-slider');
            this.$min_price = this.$el.find('.inventive-min-price');
            this.$max_price = this.$el.find('.inventive-max-price');
            var default_min_price = parseInt(this.$el.find("input.default_min_price").val())
            var default_max_price = parseInt(this.$el.find("input.default_max_price").val())
            var price_range_step = parseInt(this.$el.find("input.price_range_step").val())
            var width = this.$el.width();
            this.$el.find('.range-slider').jRange({
                from: default_min_price || 0,
                to: default_max_price || 10000,
                showScale: false,
                isRange: false,
                theme: 'inventive_slider_color',
                step: price_range_step || 100,
                width: width ? width - 15 : 300 - 15,
            });
        },
        _onChangePriceRange: function(ev) {
            ev.preventDefault();
            ev.stopPropagation();
            this.$min_price.val(parseInt($(ev.currentTarget).attr('value').split(',')[0]));
            this.$max_price.val(parseInt($(ev.currentTarget).attr('value').split(',')[1]));
        }
    });
    // WebsiteSale js inherited ........................................................
    publicWidget.registry.WebsiteSale = WebsiteSale.extend({
        events: _.extend(WebsiteSale.prototype.events, {
            'click .apply_filters': '_onClickApplyFilters',
            'click .clear_filters': '_onClickClearFilters',
            'click .product_filter_div': '_onClickFiterDiv',
            'click .input-group-appen' :  '_on_input_group_append',

        }),
        _onProductReady: function() {
            var $productCustomVariantValues = $('<input>', {
                name: 'product_custom_attribute_values',
                type: "hidden",
                value: JSON.stringify(this.rootProduct.product_custom_attribute_values)
            });
            this.$form.append($productCustomVariantValues);
            var $productNoVariantAttributeValues = $('<input>', {
                name: 'no_variant_attribute_values',
                type: "hidden",
                value: JSON.stringify(this.rootProduct.no_variant_attribute_values)
            });
            this.$form.append($productNoVariantAttributeValues);
            if (this.isBuyNow) {
                this.$form.append($('<input>', {name: 'express', type: "hidden", value: true}));
            }
            var product_id = parseInt(this.$form.find("input[name='product_id']").val(), 10) || 0;
            var quantity = this.$form.find("input.quantity") ? parseInt(this.$form.find("input.quantity").val(), 10) : 1;
            if (product_id) {
                var self = this;
                ajax.jsonRpc("/shop/cart/update_json", 'call', {
                    'product_id': product_id,
                    'add_qty': quantity,
                    'display': false,
                }).then(function(value) {
                    var $q = $(".my_cart_quantity");
                    $q.html(value.cart_quantity);
                    var $modal = self.$form.parents("#inventive_product_item_view_modal");
                    if ($modal.length) {
                        $modal.css("opacity", "0");
                        $(".modal-backdrop").css("opacity", "0");
                        setTimeout(function() {
                            $modal.css("opacity", "");
                            $(".modal-backdrop").css("opacity", "");
                        }, 2000)
                    }
                    var oe_product = self.$form.parents('.oe_product');
                    if (!oe_product.length)
                        oe_product = $('#product_detail');
                    wSaleUtils.animateClone($('.o_wsale_my_cart'), oe_product, 25, 40);
                    wSaleUtils.updateCartNavBar(value);
                });
            }
        },
        _onChangeAttribute: function (ev) {
            var $target = $(ev.currentTarget);
            ev.stopPropagation();
            ev.preventDefault();
            if ($target.is(":checked"))
                $target.parent().addClass("active");
            else
                $target.parent().removeClass("active");
        },
        _onClickApplyFilters:function(ev){
            if (!ev.isDefaultPrevented()) {
                ev.preventDefault();
            }
            $("#wsale_products_attributes_collapse").find("form").submit();
        },
        _onClickClearFilters:function(ev){
            ev.preventDefault();
            ev.stopPropagation();
            window.location = window.location.origin + window.location.pathname
        },
        _onClickFiterDiv:function(ev) {
            ev.stopPropagation();
        },
        _on_input_group_append:function(){
          var $target = $(ev.currentTarget);
            
        }
    });
    // product Lazy Loading..................................................
    publicWidget.registry.inventiveLazyLoading = publicWidget.Widget.extend({
        selector: '#inventive_lazy_loader',
        events: {
            'click .btn-primary': '_onClick',
        },
        init: function() {
            this._super.apply(this, arguments);
            this.flag = true;
            this.page = 2;
            this.href = window.location.href;
        },
        start: function() {
            if (this.href.indexOf("#") > -1) {
                var pound_attr = this.href.substring(this.href.indexOf("#"), this.href.length);
                this.href = this.href.replace(pound_attr, "")
            }
            this.href = this.href.split("?");
            var mode = this.$el.data("mode");
            if (mode == "scroll") {
                $(window).on('scroll', _.throttle(this._onScroll.bind(this), 200));
            }
        },
        inViewPort: function() {
            var element = $("#products_grid .oe_product:last-child");
            var elementTop = element.offset().top;
            var elementBottom = elementTop + element.outerHeight();
            var viewportTop = $(window).scrollTop();
            var viewportBottom = viewportTop + $(window).height();
            return elementBottom > viewportTop && elementTop < viewportBottom;
        },
        _onScroll: function() {
            if(this.inViewPort()){
                if (this.flag) {
                    this.flag = false;
                    this.$el.find(".data_loader").show();
                    this._appendProductsData();
                }
            }
        },
        _onClick: function(ev) {
            if (this.flag) {
                this.flag = false;
                this.$el.find(".data_loader").show();
                this.$el.find(".btn-primary").hide();
                this._appendProductsData();
            }
        },
        _appendProductsData: function() {
            var self = this;
            this.final_href = this.href.length > 1 ? `${ this.href[0] }/page/${ this.page }?${ this.href[ this.href.length - 1 ] }&view=inventive-lazy-load` : `${ this.href[0] }/page/${ this.page }?view=inventive-lazy-load`;
            $.get(this.final_href, function(data) {
                self.$el.find(".data_loader").hide();
                if (data) {
                    $("#products_grid .oe_product:last").after(data);
                    $("#inventive_lazy_loader .btn-primary").show();
                    self.page += 1;
                    self.flag = true;
                } else {
                    self.flag = false;
                    $("#inventive_lazy_loader").html("<h6 class='end_text'>You\'ve reached the end.</h6>");
                    $("#inventive_lazy_loader").css("background-image", "none");
                    $("#inventive_lazy_loader").css("display", "unset");
                }
            });
        }
    });
    // Product Quick View.....................................................
    publicWidget.registry.productQuickViews = publicWidget.Widget.extend({
        selector: '#products_grid',
        events: {
            'click .inventive_product_quick_view': '_onClickQuickView',
            'click .inventive_alternatives_quick_view,.inventive_accessories_quick_view': '_onClickAlternativeOrAccessoriesView',
            'click .css_quantity .qty_dec': '_onClickQtyDecrease',
            
        },
        init: function() {
            this._super.apply(this, arguments);
        },
        _onClickQuickView:function(ev){
            var $target = $(ev.currentTarget);
            var product_tmpl_id = parseInt($target.attr('product-template-id'));
            var $modal = $('#inventive_product_item_view_modal');
            $modal.modal('show').addClass("quick_view_modal").find(".modal-content").removeClass("inventive_modal_black").removeClass("fadeIn").find(".data_loader").show();
            $modal.find(".modal-body").empty();
            var url = "/shop/product/" + product_tmpl_id
            if (product_tmpl_id) {
                $.get(url, {}, function(data) {
                    if (data) {
                        var reqData = $(data).find("#product_detail");
                        $modal.find('.modal-body').html(reqData);
                        $modal.find('.carousel-indicators').addClass("vertical").addClass("invisible");
                        let $tigger = $modal.find('.tigger')
                        $tigger.trigger('click');
                        $modal.find('#o-carousel-product').addClass("animated");
                        $modal.find('.modal-content').find(".data_loader").hide();
                        $modal.find('.quick_product_redirect_link').removeClass("d-none");
                        th_scrollbar(document.querySelector('#product_details .th_product_desc p'));
                        th_scrollbar(document.querySelector('#product_details'));
                    } else {
                        console.log("data", data);
                    }
                });
            }
        },
        _onClickAlternativeOrAccessoriesView:function(ev){
            var $target = $(ev.currentTarget);
            var type = $target.data('type');
            var product_tmpl_id = $target.attr('product-template-id');
            var $modal = $('#inventive_product_item_view_modal');
            $modal.modal('show').find(".modal-content").find(".data_loader").show();
            $modal.find(".modal-body").empty();
            if (product_tmpl_id) {
                $.get("/inventive/product/extra/view/" + product_tmpl_id + "/?products_type=" + type, function(data) {
                    if (data) {
                        $modal.find('.modal-body').replaceWith(data);
                        $modal.find(".modal-content").find(".data_loader").hide();
                        var $target = $modal.find(".owl-carousel");
                        if($target.find('.oe_product').length>3){
                            $target.attr({
                                // "data-center": false,
                                'data-nav':true,
                                "data-autoplay": false,
                                "data-desktop-items": 3,
                                "data-dots": false,
                            });
                            owl_carousel($target,true);
                        }
                        else{
                            $target.removeClass("owl-carousel").addClass("d-flex justify-content-center");
                        }
                    }else {
                        console.log("...theme_inventive says....++++Something going wrong............here is data",data)
                    }
                });
            }
        },
        _onClickQtyDecrease:function(ev){
            var currentTarget = $(ev.currentTarget);
            var qty = currentTarget.parents(".css_quantity").find("input.quantity");
            if (qty.val() == "1"){
               ev.stopPropagation();
               ev.preventDefault();
            }
        },
    });
    // Setting Same events for Extra view modal
    publicWidget.registry.modalProductQuickViews = publicWidget.Widget.extend(new publicWidget.registry.productQuickViews,{
        selector:"#inventive_product_item_view_modal",
    });
    return {
        'productQuickViews':publicWidget.registry.productQuickViews,
        'inventivePriceFilter':publicWidget.registry.inventivePriceFilter,
    }
});


// About Us Page js
odoo.define('theme_inventive.aboutus_page_js', function(require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    var owl_carousel = require('theme_inventive.main_js')['owl_carousel'];
    publicWidget.registry.CompanyTeamCarousel = publicWidget.Widget.extend({
        selector: '.s_inventive_company_team',
        start: function(ev){
            if( ! $("body").hasClass('editor_enable')){
                var $target = this.$target.find(".inventive_carousel");
                var $target_clone = $target.clone().addClass("clone");
                $target.after($target_clone)
                $target_clone.addClass("owl-carousel").attr({
                    "data-desktop-items":5,
                    "data-tab-items":3,
                    "data-mobile-items":2,
                    "data-small-items":1,
                    "data-nav":true,
                });
                $target.hide();
                owl_carousel($target_clone,true);

            }else{
                var $target_clone = this.$target.find(".inventive_carousel.clone");
                var $target = this.$target.find(".inventive_carousel:not('.clone')");
                $target_clone.remove();
                $target.show();
            }
        },
    });
});
