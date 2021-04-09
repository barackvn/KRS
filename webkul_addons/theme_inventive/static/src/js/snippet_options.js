/* Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
odoo.define("theme_inventive.snippet_options_js", function(require) {
    "use strict";
    var website_options = require('website.editor.snippets.options');
    var options = require('web_editor.snippets.options');
    var publicWidget = require('web.public.widget');
    // carousel Options.......................................................
    options.registry.inventive_carousel =  options.registry.carousel.extend({
        autoplay: function (previewMode, value) {this.$target.attr('data-autoplay', value);},
        smartspeed: function (previewMode, value) {this.$target.attr('data-smartSpeed', value);},
        nav: function (previewMode, value) {this.$target.attr('data-nav', value);},
        dots: function (previewMode, value) {this.$target.attr('data-dots', value);},
        autoplaytimeout: function (previewMode, value) {this.$target.attr('data-autoplayTimeout', value);},
        animatein: function (previewMode, value) {this.$target.attr('data-animateIn', value); },
        animateout: function (previewMode, value) {this.$target.attr('data-animateOut', value);},
        animationinoff:function(previewMode,value) {this.$target.removeAttr('data-animateIn');},
        animationoutoff:function(previewMode,value) {this.$target.removeAttr('data-animateOut');},
        loop: function (previewMode, value) {this.$target.attr('data-loop', value);},

        selectClass: function (previewMode, value, $opt) {
            var $group = $opt && $opt.closest('.dropdown-submenu');
            if (!$group || !$group.length)
                $group = this.$el;
            var $lis = $group.find('[data-select-class]').addBack('[data-select-class]');
            var classes = $lis.map(function () {return $(this).data('selectClass');}).get().join(' ');
            this.$target.removeClass(classes);
            this.$target.parent().find(".owl-carousel").removeClass(classes);
            if (value) {
                this.$target.addClass(value);
                this.$target.parent().find(".owl-carousel").addClass(value);
            }
        },
        toggleClass:function(previewMode, value, $opt){
            var $lis = this.$el.find('[data-toggle-class]').addBack('[data-toggle-class]');
            var classes = $lis.map(function () {return $(this).data('toggleClass');}).get().join(' ');
            var activeClasses = $lis.filter('.active, :has(.active)').map(function () {return $(this).data('toggleClass');}).get().join(' ');
            this.$target.removeClass(classes).addClass(activeClasses);
            if (value && previewMode !== 'reset') {
                this.$target.toggleClass(value);
                this.$target.parent().find(".owl-carousel").toggleClass(value);
            }
        },
        _setActive: function () {
            this._super.apply(this, arguments);
            this.$el.find('[data-interval]').removeClass('active').filter('[data-interval=' + this.$target.attr('data-interval') + ']').addClass('active');
            this.$el.find('[data-autoplay]').removeClass('active').filter('[data-autoplay=' + this.$target.attr('data-autoplay') + ']').addClass('active');
            this.$el.find('[data-autoplayTimeout]').removeClass('active').filter('[data-autoplayTimeout=' + this.$target.attr('data-autoplayTimeout') + ']').addClass('active');
            this.$el.find('[data-smartSpeed]').removeClass('active').filter('[data-smartSpeed=' + this.$target.attr('data-smartSpeed') + ']').addClass('active');
            this.$el.find('[data-nav]').removeClass('active').filter('[data-nav=' + this.$target.attr('data-nav') + ']').addClass('active');
            this.$el.find('[data-dots]').removeClass('active').filter('[data-dots=' + this.$target.attr('data-dots') + ']').addClass('active');
            this.$el.find('[data-animateIn]').removeClass('active').filter('[data-animateIn=' + this.$target.attr('data-animateIn') + ']').addClass('active');
            this.$el.find('[data-animateOut]').removeClass('active').filter('[data-animateOut=' + this.$target.attr('data-animateOut') + ']').addClass('active');
            this.$el.find('[data-loop]').removeClass('active').filter('[data-loop=' + this.$target.attr('data-loop') + ']').addClass('active');
        },
    });
    //inventive_change_img option ...............................................
    options.registry.inventive_change_img =  options.registry.background.extend({
        background: function (previewMode, value, $opt) {
            if (previewMode === 'reset' && value === undefined) {
                this._setCustomBackground(this.__customImageSrc);
                return;
            }
            if (value && value.length) {
                // custom code starts here ..............
                var $target = this.$target.find(".img");
                if($target.length>=1){
                    $target.attr('src', value );
                    $target.removeClass('oe_custom_bg');
                    this.$target.css('background-image', '');
                    this.$target.removeClass('oe_img_bg oe_custom_bg');
                }
                // ...............end....................
            } else {
                // custom code starts here ..............
                var $target = this.$target.find(".img");
                if($target.length>=1){
                    $target.attr('src', '');
                    $target.removeClass('oe_img_bg oe_custom_bg');
                }
                // ..............end............................
            }
        },
    });
    // change  background option ................................................
    options.registry.inventive_change_background =  options.registry.background.extend({
        background: function (previewMode, value, $opt) {
            if (previewMode === 'reset' && value === undefined) {
                this._setCustomBackground(this.__customImageSrc);
                return;
            }
            if (value && value.length) {
                this.$target.css('background-image', 'url(\'' + value + '\')');
                this.$target.removeClass('oe_custom_bg').addClass('oe_img_bg');

                // custom code starts here ..............
                var $slice = this.$target.find(".slice") ;
                if($slice.length>=1){
                    $slice.css('background-image', 'url(\'' + value + '\')');
                    $slice.removeClass('oe_custom_bg').addClass('oe_img_bg');
                    this.$target.css('background-image', '');
                    this.$target.removeClass('oe_img_bg oe_custom_bg');
                }
                // ...............end....................

            } else {
                this.$target.css('background-image', '');
                this.$target.removeClass('oe_img_bg oe_custom_bg');
                // custom code starts here ..............
                var $slice = this.$target.find(".slice");
                if($slice.length>=1){
                    $slice.css('background-image', '');
                    $slice.removeClass('oe_img_bg oe_custom_bg');
                }
                // ..............end............................
            }
        },

    });
    // mega menu options................................................
    options.registry.js_get_mega_menu_category = options.Class.extend({
        start: function () {
            var self = this;
            var def = this._rpc({
                model: 'product.public.category',
                method: 'search_read',
                args: [[], ['name', 'id','parent_id']],
            }).then(function (categories) {
                var $menu = self.$el.find('[data-category-id="0"]').parent();
                categories = categories.filter(category =>  category.parent_id==false)
                _.each(categories, function (category) {
                    $menu.append($('<we-button/>', {
                        'data-category-id': category.id,
                        'data-no-preview': 'true',
                        text: category.name,
                    }));
                });
            });
            this._findLinks();
            return $.when(this._super.apply(this, arguments), def);
        },
        categoryId: function (previewMode, value, $opt) {
            value = parseInt(value);
            console.log("this.$target",this.$target);
            this.$target.attr('data-category-id', value).data('categoryId', value);
            this.$target.parent().find("span.category_id").text(value);

            this.trigger_up('content_changed', {
                editableMode: true,
                $target: this.$target,
            });
        },
        _findLinks: function () {
            this.$submenus = this.$target.find('.nav-link');
            var $el = this.$target;
        },
        _setActive: function () {
            console.log("_setActive00");

            this.megaMenu = this.megaMenu ? this.megaMenu : new publicWidget.registry.InventiveMegaMenu();
            console.log("megaMenu",this.megaMenu);
            console.log("Tartget",this.$target);
            this.megaMenu._resetMegaMenu(this.$target);

            this._refreshPublicWidgets();
            this._super.apply(this, arguments);
            this.$el.find('[data-category-id]').removeClass('active').filter('[data-category-id=' + this.$target.attr('data-category-id') + ']').addClass('active');

        },
    });

});
