/* Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

odoo.define("theme_inventive.editor_js", function(require) {
    "use strict";
    var WebsiteNavbar = require('website.navbar');
    var owl_carousel = require('theme_inventive.main_js')['owl_carousel'];
    var webEditor = require('web_editor.editor');

    var themeWebEditor = webEditor.Class.include({
        save: function (reload) {
            var self = this;
            var defs = [];
            this.trigger_up('ready_to_save', {defs: defs});
            // custom code....................
            defs.push(new Promise(resolve =>{
                $(".s_dynamic_data").empty();
                self._carousel_to_owl_carousel();
                resolve();
            }));
            // custom code END..................
            return Promise.all(defs).then(function () {
                if (self.snippetsMenu) {
                    self.snippetsMenu.cleanForSave();
                }
                return self._saveCroppedImages();
            }).then(function () {
                return self.rte.save();
            }).then(function () {
                if (reload !== false) {
                    return self._reload();
                }
            });
        },
        _carousel_to_owl_carousel:function(){
            const owl_carousel_div = "<div class='owl-carousel owl-theme s_carousel_default'/>"
            $("#wrapwrap .th_snippet .s_carousel").each(function(){
                var $source = $(this).parent();
                var $target = $source.find(".owl-carousel");

                if (!$target.length){
                    $source.find(".s_carousel").after(owl_carousel_div);
                    $target = $source.find(".owl-carousel");
                    for (let [key, value] of Object.entries($source.data())){
                        $target.attr("data-"+key,value);
                    }
                }
                $target.html($(this).find(".carousel-inner").html());
                $target.find(".carousel-item").removeClass("carousel-item active");
                $target.show().removeClass("owl-hidden");
                $(this).hide();
            });
        },
    })

    var WebsiteNavbar = WebsiteNavbar.WebsiteNavbar.include({
        _onEditMode: function () {
            this._owl_carouse_to_carousel();
            this._super();
        },
        _owl_carouse_to_carousel:function(){
            $("#wrapwrap .th_snippet .s_carousel").each(function(){
                var $source = $(this).parent();
                var $target = $source.find(".owl-carousel")
                $target.hide();
                $(this).show();
            });
        },
    });
});
