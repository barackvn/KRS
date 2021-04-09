odoo.define('theme_inventive.product_comparison', function(require) {
    'use strict';

    var core = require('web.core');
    var utils = require('web.utils');
    var qweb = core.qweb;
    var concurrency = require('web.concurrency');
    var website_sale_utils = require('website_sale.utils');
    var apply_overlay = require('theme_inventive.main_js')['apply_overlay'];
    var remove_overlay = require('theme_inventive.main_js')['remove_overlay'];
    var VariantMixin = require('sale.VariantMixin');
    var ProductComparison = require("website_sale_comparison.comparison");
    var publicWidget = require('web.public.widget');
    var ProductComparison = publicWidget.registry.ProductComparison
    var _t = core._t;


    var ThemeProductComparison = publicWidget.Widget.extend(VariantMixin, {
        xmlDependencies: ['/theme_inventive/static/src/xml/theme_inventive.xml'],
        template: 'th_product_comparison_template',
        init: function() {
            this._super.apply(this, arguments);
            this.product_data = {};
            this.comparelist_product_ids = JSON.parse(utils.get_cookie('comparelist_product_ids') || '[]');
            this.product_compare_limit = 4;
            this.guard = new concurrency.Mutex();
        },
        start: function() {
            var self = this;
            this._loadProducts(this.comparelist_product_ids).then(function () {
                self._updateContent('hide');
            });
            this._updateComparelistView();
            $(document.body).on('click', '.compare_list_products .o_remove', function(ev) {
                ev.preventDefault();
                self._removeFromComparelist(ev);
            });
            $(document.body).on('click.product_comparaison_widget', '.o_comparelist_remove', function (ev) {
                self._removeFromComparelist(ev);
                self.guard.exec(function() {
                    var new_link = '/shop/compare/?products=' + self.comparelist_product_ids.toString();
                    window.location.href = _.isEmpty(self.comparelist_product_ids) ? '/shop' : new_link;
                });
            });
            return this._super.apply(this, arguments);
        },
        destroy: function() {
            this._super.apply(this, arguments);
            $(document.body).off('.product_comparaison_widget');
        },
        handleCompareAddition: function($elem) {
            var self = this;
            if (this.comparelist_product_ids.length < this.product_compare_limit) {
                var productId = $elem.data('product-product-id');
                if ($elem.hasClass('o_add_compare_dyn')) {
                    productId = $elem.parent().find('.product_id').val();
                    if (!productId) { // case List View Variants
                        productId = $elem.parent().find('input:checked').first().val();
                    }
                }
                this.selectOrCreateProduct(
                    $elem.closest('form'),
                    productId,
                    $elem.closest('form').find('.product_template_id').val(),
                    false
                ).then(function (productId) {
                    productId = parseInt(productId, 10);
                    if (!productId) {
                        return;
                    }
                    self._addNewProducts(productId).then(function () {
                        website_sale_utils.animateClone($('#comp_menu_link'),$elem.closest('form'),5,50);
                        setTimeout(function(){
                            $('#my_account').find(".th_d_menu").removeClass("show");
                        },2000)
                    });
                });
            } else {
                this.$el.find('.comparelist_limit_warning').fadeIn();
                $("#comp_menu_link").trigger("click");
            }
        },
        _loadProducts: function(product_ids) {
            var self = this;
            return this._rpc({
                route: '/shop/get_product_data',
                params: {
                    product_ids: product_ids,
                    cookies: JSON.parse(utils.get_cookie('comparelist_product_ids') || '[]'),
                },
            }).then(function(data) {
                self.comparelist_product_ids = JSON.parse(data.cookies);
                delete data.cookies;
                _.each(data, function(product) {
                    self.product_data[product.product.id] = product;
                });
            });
        },
        _addNewProducts: function(product_id) {
            return this.guard.exec(this._addNewProductsImpl.bind(this, product_id));
        },
        _addNewProductsImpl: function (product_id) {
            var self = this;
            $('#my_account').find(".th_d_menu").addClass("show");
            if (!_.contains(self.comparelist_product_ids, product_id)) {
                self.comparelist_product_ids.push(product_id);
                if (_.has(self.product_data, product_id)){
                    self._updateContent();
                } else {
                    return self._loadProducts([product_id]).then(function () {
                        self._updateContent();
                        self._updateCookie();
                    });
                }
            }
            self._updateCookie();
        },
        _updateContent: function(force) {
            var self = this;
            var $target = this.$el.find(".compare_list_products");
            $target.empty();
            _.each(this.comparelist_product_ids, function(res) {
                var $template = self.product_data[res].render;
                $target.append($template);
            });
        },
        _updateSliderContent:function(force){
            $('.dynamic_cart_content').html(this.$el);
        },
        _removeFromComparelist: function (e) {
            this.guard.exec(this._removeFromComparelistImpl.bind(this, e));
        },
        _removeFromComparelistImpl: function (e) {
            this.comparelist_product_ids = _.without(this.comparelist_product_ids, $(e.currentTarget).data('product_product_id'));
            $(e.currentTarget).parents('.o_product_row').remove();
            $('.comparelist_limit_warning').hide();
            this._updateCookie();
            this._updateContent('show');
        },
        _updateCookie: function() {
            document.cookie = 'comparelist_product_ids=' + JSON.stringify(this.comparelist_product_ids) + '; path=/';
            this._updateComparelistView();
        },
        _updateComparelistView: function() {
            $('.product_comp_quantity').text(this.comparelist_product_ids.length);
            this.$el.find('.comparelist_button').removeClass('d-block');
            if (_.isEmpty(this.comparelist_product_ids)) {
                this.$el.find('.comparelist_button').addClass('d-none');
                this.$el.find('.comparelist_limit_warning').show();
                this.$el.find('.comparelist_limit_warning span').html('<i class="fa fa-warning text-danger" role="img" aria-label="Warning" title="Warning"></i>' + "  Your compare list is Empty");
            } else {
                if (this.comparelist_product_ids.length >= 2) {
                    this.$el.find('.comparelist_button').addClass('d-block');
                    this.$el.find('.comparelist_button a').attr('href', '/shop/compare/?products=' + this.comparelist_product_ids.toString());

                    this.$el.find('.comparelist_limit_warning').hide();
                    this.$el.find('.comparelist_limit_warning span').html('<i class="fa fa-warning text-danger" role="img" aria-label="Warning" title="Warning"></i>' + "  You can compare max 4 products.");
                }
                else{
                    this.$el.find('.comparelist_limit_warning').show();
                    this.$el.find('.comparelist_button').addClass('d-none');
                    this.$el.find('.comparelist_limit_warning span').html('<i class="fa fa-warning text-danger" role="img" aria-label="Warning" title="Warning"></i>' + "  There must be atlest 2 products to compare.");
                }
            }
        },
    });
    // override core events and add to compare functionality
    publicWidget.registry.ProductComparison = ProductComparison.extend({
        selector: '.product_comp_menu',
        read_events: {
            "click #comp_menu_link": "_open_comparison_product_list",
        },
        start: function() {
            var self = this;
            this.main_nav = $('#oe_main_menu_navbar');
            this.productComparison = new ThemeProductComparison(this);
            this.productComparison.willStart().then(function () {
                if (self.productComparison__parentedDestroyed) {
                    return;
                }
                self.productComparison.renderElement();
                self.productComparison.start();
            });
            $('.o_add_compare, .js_main_product .o_add_compare_dyn').on('click', function(ev){
                self._onClickAddCompare(ev);
            });
        },
        _open_comparison_product_list: function(ev) {
            var self = this;
            var $slider = $("#th_mycart_slider");
            $slider.addClass("slide_left");
            apply_overlay();
            $("#wrapwrap").on('click','.overlay, #th_mycart_slider .close_icon',function(){
                remove_overlay();
                $slider.removeClass("slide_left");
                $slider.find(".dynamic_cart_content").html("<div class='data_loader' data-loader='wave'></div>");
            });
            if (this.main_nav && this.main_nav.length !=0)
                $slider.css("top",this.main_nav.height() + "px");

            $('.dynamic_cart_content').html(this.productComparison.$el);
        },
        _onClickAddCompare: function (ev) {
            this.productComparison.handleCompareAddition($(ev.currentTarget));
        },
        _onClickComparelistTr: function (ev) {
            var $target = $(ev.currentTarget);
            $($target.data('target')).children().slideToggle(100);
            $target.find('.fa-chevron-circle-down, .fa-chevron-circle-right').toggleClass('fa-chevron-circle-down fa-chevron-circle-right');
        },
    });
});
