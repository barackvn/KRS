/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('website_collectional_page.wk_collection', function(require) {
            "use strict";
            var ajax = require('web.ajax');

            $(document).ready(function(){

                $('[id^=simpleCarousel]').carousel({
                  interval: 10000
                })

                $('[id^=simpleCarousel] .carousel-item').each(function(){
                  var next = $(this).next();

                  if (!next.length) {
                    next = $(this).siblings(':first');
                  }
                  next.children(':first-child').clone().appendTo($(this));
                  if (next.next().length>0) {
                    next.next().children(':first-child').clone().appendTo($(this));
                  }
                  else {
                  	$(this).siblings(':first').children(':first-child').clone().appendTo($(this));
                  }
                });

        });
});
