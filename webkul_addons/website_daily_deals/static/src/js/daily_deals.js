odoo.define("website_daily_deals.daily_deals_js", function (require) {
"use strict";

    var ajax = require('web.ajax');
    var sAnimations = require('website.content.snippets.animation');

    $(document).ready(function() {
        // .............Daily Deal Slider...............................
		var options = {
			autoplay:true,
			loop:false,
      center:true,
			items:5,
			nav:true,
            dots:true,
            nav:true,
            smartSpeed:1000,
            autoWidth:false,
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
                998 : {
                    items:5
                }
            }
		}
		$(".deals_owl_carousel").owlCarousel(options);

        $(".deal_main_div").each(function(){
            var end_date= $(this).find("input[name='end_date']").val();
            var deal_id = parseInt($(this).find("input[name='deal_id']").val(),10);
            var state = $(this).find("input[name='state']").val()
            var msg_before_offset= $(this).find("input[name='msg_before_offset']").val()
            if(state=="validated"){
                $(this).find(".deal_countdown_timer").countdown({
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
                    ajax.jsonRpc('/daily/deal/expired/'+deal_id, 'call', {})
                    .then(function (res) {
                        console.log(res);
                        if(res){
                            window.location.reload();
                        }
                    });
                });
                if(msg_before_offset){
                    var $target = $(this).find(".msg_before_exp");
                    $(this).find(".expiry_messages").countdown({
                        date: msg_before_offset,
                        offset: +0,
                        day: 'Day',
                        days: 'Days'
                    },function () {
                        $target.css('visibility','visible');
                    });
                }

            }
        });
        $('.deal_product_quick_view').on('click',function(){
            var product_tmpl_id     = parseInt($(this).attr('product-template-id'));
            var product_variant_id  = parseInt($(this).attr('product-product-id'));
            var url = "/shop/product/"+product_tmpl_id
            if (product_tmpl_id){
                $.get(url,{
                },function (data){
                    if (data) {
                        data = $(data).find("#product_detail");
                        $('#deal_product_item_view_modal').modal('show');
                        $('#deal_product_item_view_modal .modal-body').html(data);
                        $('#deal_product_item_view_modal').find("#product_detail>.row:nth-child(1)").hide();
                    }
                });
            }
        });

    });

});
