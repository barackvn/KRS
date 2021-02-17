/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* @License       : https://store.webkul.com/license.html */

odoo.define('marketplace_ajax_login.marketplace_ajax_login', function(require) {
    var ajax = require('web.ajax');

    function custom_mark(element_id, status) {
        if (status == true) {
            element_id
                .parent()
                .addClass('has-error has-feedback')
                .append("<span class='fa fa-times form-control-feedback'></span>");

        } else if (status == false) {
            element_id
                .parent()
                .removeClass('has-error  has-feedback')
                .children("span")
                .remove();
        }
    }

    function custom_msg(element_id, status, msg) {
            if (status == true) {
                element_id.empty().append("<div class='alert alert-danger text-center' id='Wk_err'>" + msg + "<button type='button' class='close' data-dismiss='alert' aria-label='Close'><span class='res fa fa-times ' aria-hidden='true'></span></button></div>");
            }
            if (status == false) {
                element_id.empty();
            }
            return true;
        }

    $(document).ready(function() {

        function link_provider(arg, link) {
            if ($("a").hasClass(arg) == true) {
                $('.' + arg).attr('href', link);
            }
            return true
        }

        $('#is_seller').on('click',function(ev){
            var mp_ajax_is_seller = $(document).find('#is_seller').prop('checked');
            var $form = $(this).closest('form')
            var $google = $form.find('.btn-googleplus');
            var $facebook = $form.find('.btn-facebook');
            var $odoo = $form.find('.btn-odoo');

            ajax.jsonRpc('/signup_as_seller_link/', 'call', {
                    'is_seller':mp_ajax_is_seller,
                    'url_google': $google.attr('href'),
                    'url_fb': $facebook.attr('href'),
                    'url_odoo': $odoo.attr('href'),
                })
                .then(function(response){
                    $.each(response, function(key, value)
                    {
                        if(key == 'url_google'){
                            $google.attr('href',value);
                        }
                        if(key == 'url_fb'){
                            $facebook.attr('href',value);
                        }
                        if(key == 'url_odoo'){
                            $odoo.attr('href',value);
                        }

                    });
                });
        });

    	var wk_mp_block_ui;
    	// Pop up ajax login form when user not logged in
        // check ajax element in dom and load the controller
        var ajax_element = document.getElementById('wk_ajax_login_doc');
        if (ajax_element != null) {
            ajax.jsonRpc('/web/session/wk_check', 'call').then(function(res) {
                wk_mp_block_ui = res["wk_block_ui"]
                if (! res)
                {
                    if (wk_mp_block_ui)
                    {
                        $('#wk_Modal_login').modal({
                            keyboard: false,
                            backdrop: 'static'
                        });
                    }
                    $("<div id='wk_ajax_loader'/>").appendTo('body');

                    ajax.jsonRpc('/wk_modal_login/', 'call', {
                            'url': location.href,
                            'name': 'parent'
                        })
                        .then(function(response) {
                            $.each(response, function(key, value) {
                                if (value.validation_endpoint.search("facebook") > 0) {
                                    link_provider('btn-facebook', value.auth_link);
                                }
                                if (value.validation_endpoint.search("googleapis") > 0) {
                                    link_provider('btn-googleplus', value.auth_link);
                                }
                                if (value.validation_endpoint.search("odoo") > 0) {
                                    link_provider('btn-odoo', value.auth_link);
                                }

                            });
                        });
                    $('input[name="redirect"]').val(window.location.pathname);
                    var element = document.getElementById("wk_ajax_loader");
                    element.parentNode.removeChild(element);
                    $('#wk_Modal_login').appendTo('body').modal('show');
                }
            });
        }

        $('[data-toggle="popover"]').popover({container: '.ajax_url_info'});

		$('#linksignup').on('click', function() {
            if (wk_mp_block_ui)
            {
                $('#wk_Modal_signup').modal({
                    keyboard: false,
                    backdrop: 'static'
                });
            }
            $('#wk_Modal_login').modal('hide');
            $('#wk_Modal_signup').appendTo('body').modal('show');
        });

        $('#login_menu').on('click', function(ev) {
        	ev.preventDefault();
	    	ev.stopPropagation();
	    	ev.stopImmediatePropagation();
            if (wk_mp_block_ui)
            {
                $('#wk_Modal_login').modal({
                    keyboard: false,
                    backdrop: 'static'
                });
            }
            $("<div id='wk_ajax_loader'/>").appendTo('body');

            ajax.jsonRpc('/wk_modal_login/', 'call', {
                    'url': location.href,
                    'name': 'parent'
                })
                .then(function(response) {
                    $.each(response, function(key, value) {
                        if (value.validation_endpoint.search("facebook") > 0) {
                            link_provider('btn-facebook', value.auth_link);
                        }
                        if (value.validation_endpoint.search("googleapis") > 0) {
                            link_provider('btn-googleplus', value.auth_link);
                        }
                        if (value.validation_endpoint.search("odoo") > 0) {
                            link_provider('btn-odoo', value.auth_link);
                        }

                    });
                });
            $('input[name="redirect"]').val(window.location.pathname);
            var element = document.getElementById("wk_ajax_loader");
            element.parentNode.removeChild(element);
            $('#wk_Modal_login').appendTo('body').modal('show');
        });

    	//Is seller and Marketplace Terms and conditions
	    var term_condition = $('#mp_terms_conditions_for_mp_ajax').data("terms");
		$(document).find("#mp_ajax_mp_t_and_c").html(term_condition);
		if ($('#is_seller').prop('checked') && $(term_condition).text().trim().length > 0){
			$(document).find("#mp_ajax_mp_t_and_c").slideDown();
			$(document).find("#t_and_c_label").show();
		}

		// Ajax login
		$('#wk_login_button').on('click', function(ev) {
			if (wk_mp_block_ui)
            {
                $('#wk_Modal_login').modal({
                    keyboard: false,
                    backdrop: 'static'
                });
            }
			ev.preventDefault();
	    	ev.stopPropagation();
	    	ev.stopImmediatePropagation()
            $('#wk_login_error').empty();
            var login = $(this).parent().parent().parent().find('#ajax_login');
            var password = $(this).parent().parent().parent().find('#ajax_password');
            var database = $(this).parent().parent().parent().find('.ajax_db :selected').val();
            var redirect = window.location.pathname;
            var input = {
                login: login.val(),
                password: password.val(),
                db: database,
                // redirect:redirect
            };
            $("<div id='wk_ajax_loader'/>").appendTo('body');
            ajax.jsonRpc('/shop/login/', 'call', input)
                .then(function(response) {

                    var element = document.getElementById("wk_ajax_loader");

                    if (response['uid'] != false) {
	                    redirect_url = window.location.origin + response["redirect"]
	                    window.location.href = redirect_url;
                        $(window).on('load', function() {});
                    }
                    else {
                        element.parentNode.removeChild(element);
                        custom_msg($('#wk_login_error'), true, "Wrong login/password");
                        custom_mark($('.demo_loginclass'), true);
                        $('#Wk_err button').on('click', function() {
                            custom_msg($('#wk_login_error'), false, "");
                            custom_mark($('.demo_loginclass'), false);
                        });
                    }
                });
        });


		// Ajax signup
        $('#wk_signup_button').off('click')
	    $('#wk_signup_button').on('click', function(ev) {
	    	ev.preventDefault();
	    	ev.stopPropagation();
	    	ev.stopImmediatePropagation();
	        var name = $(this).parent().parent().parent().parent().find('#signup_name');
	        var login = $(this).parent().parent().parent().parent().find('#signup_login');
	        var password = $(this).parent().parent().parent().parent().find('#signup_password');
	        var confirm_password = $(this).parent().parent().parent().parent().find('#signup_confirm_password');
	        var mp_ajax_is_seller = $(document).find('#is_seller').prop('checked');
            var mp_country_id = String($(document).find('#country_id').val());
            var mp_profile_url = String($(document).find('#profile_url').val());
            var mp_terms_conditions = $(document).find('#mp_terms_conditions').prop('checked');
            var redirect = window.location.pathname;
	        var input = {
	            'login': login.val(),
	            'password': password.val(),
	            'confirm_password': confirm_password.val(),
	            'db': '',
	            'name': name.val(),
	            'redirect': '/shop',
                // 'redirect': redirect,
	        };
	        if (mp_ajax_is_seller){
                input['is_seller'] = mp_ajax_is_seller;
                input['country_id'] = mp_country_id;
                input['url_handler'] = mp_profile_url;
                input['mp_terms_conditions'] = mp_terms_conditions;
            }
            $("<div id='wk_ajax_loader'/>").appendTo('body');
	        ajax.jsonRpc('/website_ajax_login/signup', 'call', input)
	            .then(function(res) {

                    var element = document.getElementById("wk_ajax_loader");

	                list_res = res.error.split(",");
	                if (typeof(res['uid']) != "undefined") {
	                    redirect_url = window.location.origin + res["redirect"]
	                    window.location.href = redirect_url;
                        $(window).on('load', function() {});
	                }
                    else{
                        element.parentNode.removeChild(element);
    	                var responses = [
    	                    "all fields are madetory",
    	                    "email is not valid",
    	                    "already register",
    	                    "password not match",
    	                    "--site is under construction please try after sometimes---",
                            "Please enter profile url correctly!",
                            "Sorry, this profile url is not available.",
    	                ];
    	                if (list_res.indexOf("filled") > 0) {
    	                    custom_msg($('#wk_signup_error'), true, responses[0]);
    	                    var a = jQuery("#wk_Modal_signup input:text[value=''] ,#wk_Modal_signup input:password[value=''] ");
    	                    a.each(function(index) {
    	                        $(this).parent()
    	                            .addClass('has-error has-feedback')
    	                            .append("<span class='fa fa-times form-control-feedback'></span>");

	                        });
	                    }
    	                if (list_res.indexOf("email") > 0) {
    	                    custom_msg($('#wk_signup_error'), true, responses[1]);
    	                }
    	                if (list_res.indexOf("register") > 0) {
    	                    custom_msg($('#wk_signup_error'), true, responses[2]);
    	                }
    	                if (list_res.indexOf("confirm_password") > 0) {
    	                    custom_msg($('#wk_signup_error'), true, responses[3]);
    	                }
                        if (list_res.indexOf("url_incorrect") > 0) {
    	                    custom_msg($('#wk_signup_error'), true, responses[5]);
    	                }
                        if (list_res.indexOf("url_not_available") > 0) {
    	                    custom_msg($('#wk_signup_error'), true, responses[6]);
    	                }
                    }
	            });
	        return false;
	    });
		// Dynamic text field add/remove
		var email_counter = 2;

	    $("#add-btn").click(function () {
			if(email_counter>10){
		    	alert("You can invite Only 10 email.");
		        return false;
			}
			var new_email_box = $(document.createElement('div')).attr("id", 'email-box-div' + email_counter);
			new_email_box.addClass("input-group has-feedback mt8");
			new_email_box.after().html('<span class="input-group-addon"><i class="fa fa-envelope"/></span><input class="form-control" name="Email" placeholder="Email" type="textbox" id="email-box' + email_counter + '"/></div>');

			new_email_box.appendTo("#email-set");
			email_counter++;
			if (email_counter > 1)
				$("#remove-btn").removeClass("disabled");
			if(email_counter>10)
		    	$("#add-btn").addClass("disabled");
			else
				$("#add-btn").removeClass("disabled");
	     });

	    $("#remove-btn").click(function () {
			if(email_counter==1){
		        alert("No more email-box to remove.");
		        return false;
		    }
		    email_counter--;
	        $("#email-box-div" + email_counter).remove();
	        if (email_counter < 11)
				$("#add-btn").removeClass("disabled");
	        if(email_counter==1)
		    	$("#remove-btn").addClass("disabled");
			else
				$("#remove-btn").removeClass("disabled");
	    });
		$("#get-amail-btn").click(function () {
			var msg = ' Invitation is sending to following mail(s) ';
			for(i=1; i<email_counter; i++){
		   	  msg += "\n Email-" + i + " : " + $('#email-box' + i).val();
			}
	    	alert(msg);
	    });
    });
});
