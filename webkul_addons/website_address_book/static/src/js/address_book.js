odoo.define('website_address_book.address_book', function (require) {
'use strict';

    var ajax = require('web.ajax');
    // var base = require("web_editor.base");

    $(document).ready(function() {
        $('.oe_cart').on('click', '.js_change_billing', function() {
          if (!$('body.editor_enable').length) {
            var $old = $('.all_billing').find('.card.border_primary');
            $old.find('.btn-inv').toggle();
            $old.addClass('js_change_billing');
            $old.removeClass('border_primary');

            var $new = $(this).parent('div.one_kanban').find('.card');
            $new.find('.btn-inv').toggle();
            $new.removeClass('js_change_billing');
            $new.addClass('border_primary');

            var $form = $(this).parent('div.one_kanban').find('form.d-none');
            $.post($form.attr('action'), $form.serialize()+'&xhr=1');
          }
        });

        $('.a-delete').on('click', function(e) {
            var partner_id = $(this).parents('.one_kanban').find('input[name=partner_id]').val();
            ajax.jsonRpc("/delete/address", 'call', {'partner_id':partner_id})
                .then(function (data) {
                    location.reload();
                });
        });

    })

});
