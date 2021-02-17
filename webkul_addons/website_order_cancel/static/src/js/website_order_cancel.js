odoo.define('website_order_cancel.website_order_cancel', function(require) {
    "use strict";
    var ajax = require('web.ajax');
    $(document).ready(function() {
        $('.o_portal_wrap').each(function() {
            var oe_website_sale = this;
            $(oe_website_sale).on('click', '#cancel_btn', function(e) {
                var $form = $(this).closest('tr');
                var order_id = parseInt($form.find('input[type="hidden"][name="order_id"]').first().val(), 10);
                if (!order_id)
                {
                    order_id = $('.order_id').val()
                }
                ajax.jsonRpc("/cancel/order/", 'call', { 'order_id': order_id,'view_type':($(this).hasClass('btn-cancel')) })
                .then(function(vals) {
                    var $modal = $(vals);
                    $modal.appendTo(oe_website_sale)
                        .modal('show')
                        .on('hidden.bs.modal', function() {
                            $(this).remove();
                        }); 
                });
            });

            $(oe_website_sale).on('click', '#cancel_order', function(e) {
                console.log('=========')
                var $form = $(this).closest('tr');
                var order_id = $("#order_id").val();
                var reason_id = $("#resaon_id").val();
                var remark = $("#remark").val();
                var view_type = $("#view_type").val();
                if ($("#reason-error").hasClass('o_has_error')){
                    $("#reason-error").removeClass('o_has_error').find('.form-control').removeClass('is-invalid');
                }
                if ($("#remark-error").hasClass('o_has_error')){
                    $("#remark-error").removeClass('o_has_error').find('.form-control').removeClass('is-invalid');
                }
                if (reason_id && remark){
                    ajax.jsonRpc("/cancel/order/confirm", 'call', { 'order_id': order_id ,'reason_id':reason_id, 'remark': remark})
                    .then(function(vals) {
                        $('#cancel_modal').modal('hide');
                        if (view_type){
                            location.reload();
                        }
                        else{
                            location.replace(location.href + '/#additional-remark');
                        }
                    });
                }
                else{
                    if (!reason_id)
                    {
                        $("#reason-error").addClass('o_has_error').find('.form-control').addClass('is-invalid');
                    }
                    else if(!remark)
                    {
                        $("#remark-error").addClass('o_has_error').find('.form-control').addClass('is-invalid');
                    }
                }
            });

        });
    });
});