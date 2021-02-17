/* Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
odoo.define('website_voucher.website_voucher', function (require) {
	'use strict';

	var publicWidget = require('web.public.widget');
	publicWidget.registry.websiteCoupon = publicWidget.Widget.extend({
		selector: '.oe_website_sale',
		events: {
			'click .wk_voucher': '_onClickApplyVocuher',
			'click .copy_code': '_onClickCopyCode',
			'keyup #voucher_8d_code': '_onKeyUpVoucherCode',
			// 'change .oe_cart input.js_quantity[data-product-id]':'_onChangeUpdateVoucher'
		},
		_onClickApplyVocuher: function (ev) {
			ev.preventDefault();
			this.ApplyVoucher();
		},
		ApplyVoucher() {
			var secret_code = $("#voucher_8d_code").val();
			this._rpc({
				route: "/website/voucher/",
				params: {
					secret_code: secret_code
				},
			}).then(function (result) {
				if (result['status']) {
					$(".success_msg").css('display', 'block')
					$(".success_msg").html(result['message']);
					$(".success_msg").fadeOut(3000);
					$(location).attr('href', "/shop/cart");
				}
				else {
					$(".error_msg").css('display', 'block')
					$(".error_msg").html(result['message']);
					$(".error_msg").fadeOut(5000);
				}
			});
		},
		_onClickCopyCode: function (ev) {
			var $fa = $(ev.currentTarget);
			var $temp = $("<input>");
			$("body").append($temp);
			$temp.val($fa.prev().text()).select();
			document.execCommand("copy");
			$temp.remove();
			$('.copy_code').text("Copy Code");
			$fa.text("Code Copied");
		},
		_onKeyUpVoucherCode: function(ev){
			if (ev.keyCode == 13) {
				this.ApplyVoucher();
			}
		},
		_onChangeUpdateVoucher:function(ev) {
			var $self = this
			setTimeout(function () {
				$self._rpc({
					route: "/voucher/validate/cart_change",
					params: {},
				}).then(function (data) {
					if (data) {
						location.reload();
					}
					});
			}, 500);
		},
	});
});
