/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('website_360degree_view.website_360degree_view', function (require)
    {
		$(document).ready(function() {
        "use strict";
        var ajax = require('web.ajax');
	    

	    
		$('#360degree_btn,#360degree_btn2').on('click',function(e)
		{
			
			var product_id = parseInt($(this).find('.360_product_id').first().val(),10);
			
			ajax.jsonRpc("/shop/360view/", 'call', {'product_id': product_id})
			.then(function (vals)
			{  
	            var $modal = $(vals);
	            $modal.appendTo('#wrapwrap').modal('show').on('hidden.bs.modal', function () {
	                    $(this).remove();
	                });
	        });
		});
	});
});
