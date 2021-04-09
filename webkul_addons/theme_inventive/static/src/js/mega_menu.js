odoo.define('theme_inventive.mega_menus_js', function(require) {
    'use strict';
    var publicWidget = require('web.public.widget');

    publicWidget.registry.InventiveMegaMenu = publicWidget.Widget.extend({
        selector : ".js_get_dynamic_menu",
        read_events: {
            'mouseenter .nav-tabs .nav-link': '_onMouseEnter',
        },
        init:function(){
            this._super.apply(this, arguments);
        },
        start: function () {
            // if($("body").hasClass("editor_enable")){
            //     console.log("editor_enable");
                this._resetMegaMenu();
            // }
        },
        _resetMegaMenu:function($target=false){
            $target = $target ? $target : this.$target;
            var template        = $target.parent().find('span.menu_template').text() || false;
            var category_id     = $target.parent().find('span.category_id').text() || 0;
            $target.parent().find('input.menu_template').val(template);
            // $target.attr('contenteditable', 'True'); // Prevent user edition
            if(template && category_id != 0) {
                $.get("/menu/dynamic", {
                    template    :   template,
                    category_id :   category_id,
                },function(data) {
                    $target.html(data);
                    $target.attr('contenteditable', 'False');
                });
            }
        },
        destroy: function (){
            this._super.apply(this, arguments);
        },
        _onMouseEnter:function(ev){
            $(ev.currentTarget).tab("show");
        },
    });

    publicWidget.registry.inventiveMega = publicWidget.Widget.extend({
        selector:"#top_menu",
        read_events:{
            "mouseenter .inventive_mega_menu.show_on_hover":"_onMouseEnter",
            "mouseleave .inventive_mega_menu.show_on_hover":"_onMouseLeave",
            "click .inventive_mega_menu": "_onMenuClick",
            "click .inventive_mega_menu .o_mega_menu a" : "_onSubMenuClick",
        },
        start:function(){
            this._super.apply(this,arguments);
            this.editor_mode = $("body").hasClass("editor_enable");
            this.mobile_mode = $(window).innerWidth() < 768;

        },
        _onMouseEnter:function(ev){
            if(!this.editor_mode && !this.mobile_mode){
                var currentTarget = $(ev.currentTarget);
                var dropdownMenu = currentTarget.find('.dropdown-menu.o_mega_menu');
                currentTarget.addClass('show');
                dropdownMenu.find(">section").show();
                dropdownMenu.stop(true, true).delay(300).slideDown(200);
            }
        },
        _onMouseLeave:function(ev){
            if(!this.editor_mode && !this.mobile_mode){
                var currentTarget = $(ev.currentTarget);
                var dropdownMenu = currentTarget.find('.dropdown-menu.o_mega_menu');
                currentTarget.removeClass('show');
                dropdownMenu.stop(true, true).delay(200).slideUp("show");
            }
        },
        _onMenuClick:function(ev){
            // if(this.mobile_mode){
                var currentTarget = $(ev.currentTarget);
                var dropdownMenu = currentTarget.find('.dropdown-menu.o_mega_menu');
                currentTarget.addClass('show');
                dropdownMenu.find(">section").show();
                if (currentTarget.parents("#top_menu_collapse").hasClass("slide_right")) {
                    dropdownMenu.find("a:not('.dropdown-close')").click(function(e) {
                        e.stopPropagation();
                    });
                }
            // }
        },
        _onSubMenuClick:function(ev){
            ev.stopPropagation();
        }
    });
});
