odoo.define('webiste_stock_notifiy.notify', function(require) {
    "use strict";

    var ajax = require('web.ajax');

    $(document).ready(function() {
        $('.oe_website_sale').each(function() {
            var oe_website_sale = this;

            $(oe_website_sale).on('keypress', '.wk_input_email', function(e) {
                var $form = $(this).closest('form');
                var $submit_button = $form.find('a.btn').first();
                if (e.which == 13) {
                    $submit_button.click();
                }
            });

            $(oe_website_sale).on("click", ".submit_notify_reg", function() {
                var $form = $(this).closest('form');
                var $data = $form.find('.wk_notify_main').first();

                var pageURL = $(location).attr("href");
                var product_id = $data.attr('id');
                var email = $data.find('.wk_input_email').val();

                if (EmailCheck($form, email)) {
                    var vals = { 'product_id': product_id, 'email': email, 'pageURL': pageURL }
                    ajax.jsonRpc('/website/stock_notify/', 'call', vals)
                    .then(function(res) {
                        if (res) {
                            $data.hide();
                            $form.find('.div_message_notify').first().show();
                        }
                    })
                }
            });

            $(oe_website_sale).on("click", ".submit_notify_pub", function() {
                var $form = $(this).closest('form');
                var $data = $form.find('.wk_notify_main').first();

                var pageURL = $(location).attr("href");
                var product_id = $data.attr('id');
                var email = $data.find('.wk_input_email').val();
                var name = $data.find('.wk_input_name').val();

                var name_check = NameCheck($form, name);
                var email_check = EmailCheck($form, email);

                if ((name_check) && (email_check)) {
                    var vals = { 'product_id': product_id, 'email': email, 'pageURL': pageURL, 'name': name }
                    ajax.jsonRpc('/website/stock_notify/', 'call', vals)
                    .then(function(res) {
                        if (res) {
                            $data.hide();
                            $form.find('.div_message_notify').first().show();
                        }
                    })
                }
            });

            function NameCheck($form, name) {
                if (!name) {
                    $form.find('.wk_input_name').parent().first().addClass('has-error');
                    $form.find('.name_msg').first().show();
                    return false;
                } else {
                    $form.find('.wk_input_name').parent().first().removeClass('has-error');
                    $form.find('.name_msg').first().hide();
                    return true;
                }
            }

            function EmailCheck($form, email) {
                if (!ValidateEmail(email)) {
                    $form.find('.wk_input_email').parent().first().addClass('has-error');
                    $form.find('.email_msg').first().show();
                    return false;
                } else {
                    $form.find('.wk_input_email').parent().first().removeClass('has-error');
                    $form.find('.email_msg').first().hide();
                    return true;
                }
            }

            function ValidateEmail(email) {
                var expr = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
                return expr.test(email);
            }
        });
    });
});

/* Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
