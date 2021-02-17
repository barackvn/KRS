odoo.define('website.website', function (require) {
	"use strict";
/* Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
    /* See LICENSE file for full copyright and licensing details. */
	var ajax = require('web.ajax');
	$(document).on('click', '.wk_maintenance_subscriber', function (e) {
		var email = $(this).parent().parent().parent().find('#wk_subscriber_email').val();
		var super_elm = $(this).parent().parent().parent();
		if (EmailCheck(super_elm, email)) {

			ajax.jsonRpc("/subscriber/email", 'call', {
				'email': email,

			})
				.then(function (data) {
					if (data == 'new_customer') {
						super_elm.find('.wk_valid_email_msg').first().slideDown();
					} else if (data == 'already_exists') {
						super_elm.find('.wk_exists_email_msg').first().slideDown();
						super_elm.find('.wk_invalid_email_msg').first().slideUp();
						super_elm.find('.wk_valid_email_msg').first().slideUP();
					}

				});
		}

		function EmailCheck(super_elm, email) {
			if (!ValidateEmail(email)) {
				super_elm.find('.wk_valid_email_msg').first().slideUp();
				super_elm.find('#wk_subscriber_email').addClass('has-error');
				super_elm.find('.wk_invalid_email_msg').first().slideDown();
				super_elm.find('.wk_exists_email_msg').first().slideUp();
				return false;
			} else {
				super_elm.find('#wk_subscriber_email').removeClass('has-error');
				super_elm.find('.wk_invalid_email_msg').slideUp();
				super_elm.find('.wk_exists_email_msg').first().slideUp();
				super_elm.find('#wk_subscriber_email').val('');
				return true;
			}
		}

		function ValidateEmail(email) {
			var expr = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
			return expr.test(email);
		}
	});
});