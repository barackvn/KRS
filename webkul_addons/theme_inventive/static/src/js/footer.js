/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

odoo.define("theme_inventive.footer_js", function(require) {
    "use strict";
    var ajax = require('web.ajax');
    var base = require('web_editor.base');
    var core = require('web.core');
    var utils = require('web.utils');
    var _t = core._t;

    $(document).ready(function(){
        var text_color="#434b53";
        var white = "#ffffff";
        var facebook="#3B5998";
        var twitter="#1DA1F2";
        var google="#DB4437";
        var linkedin="#0077B5";
        var youtube="#c4302b";
        var instagram="#3f729b";
        var github= "#211F1F";
        var odoo = "#875A7B"
        $(".fa-facebook").parent().hover(function(e){
            $(this).css('background-color',facebook);
        },function(){
            $(this).css('background-color',"");
        });

        $(".fa-twitter").parent().hover(function(e){
            $(this).css('background-color',twitter);
        },function(){
            $(this).css('background-color',"");
        });

        $(".fa-google-plus").parent().hover(function(e){
            $(this).css('background-color',google);
        },function(){
            $(this).css('background-color',"");
        });

        $(".fa-linkedin").parent().hover(function(e){
            $(this).css('background-color',linkedin);
        },function(){
            $(this).css('background-color',"");
        });
        $(".fa-youtube-play").parent().hover(function(e){
            $(this).css('background-color',youtube);
        },function(){
            $(this).css('background-color',"");
        });
        $(".fa-github").parent().hover(function(e){
            $(this).css('background-color',github);
        },function(){
            $(this).css('background-color',"");
        });
        $(".fa-instagram").parent().hover(function(e){
            $(this).css('background-color',instagram);
        },function(){
            $(this).css('background-color',"");
        });
        $(".o_custom_icon").parent().hover(function(e){
            $(this).css('background-color',odoo);
        },function(){
            $(this).css('background-color',"");
        });

    });

});
