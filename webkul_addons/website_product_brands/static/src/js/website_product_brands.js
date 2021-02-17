/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
$(document).ready(function () {

    $('.wk_horizontal_categories_link').hover(function() {
        if(!$(this).hasClass('hoverd'))
        {
            $(this).parent().find('.wk_horizontal_cart').slideDown('slow');
        }
    },function(){
        $(this).parent().find('.wk_horizontal_cart').slideUp('slow');
    });

    $('.wk_horizontal_cart').hide();
    if($('.products_brands_filter input[type="checkbox"]').is(":checked")){
        $('.horizontal_category_unlink_list').show();
    }

    $('.products_brands_filter input[name="attrib_brand"]').on('click',function(){
        var brands = $('.products_brands_filter').data('brands');
        var brand= $(this).data('brand');
    });

    $('.oe_website_sale').each(function () {
        var oe_website_sale = this;
        console.log($('.products_brands_filter').find("input[name='attrib_brand']:checked"));
        $('a.wk_brand').on('change click', function () {
            var wk_brand = $(this).data('wk_brand');
            $.each($('.products_brands_filter').find("input[name='attrib_brand']:checked"),
            function(){
                if (wk_brand==$(this).data('brand')){
                    $(this).click();
                }
            });
        });
    });

});
