/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : https://store.webkul.com/license.html/ */

odoo.define('advance_signup.adv_signup', function (require) {

    $(document).ready(function(){

        "use strict";
        var ajax = require('web.ajax');
        var core = require('web.core');
        var _t = core._t;
        // if(!$('.adv_input_row').length) {
        //     return $.Deferred().reject("DOM doesn't contain '.adv_input_row'");
        // }

        $('.adv_input_row').each(function () {
            var adv_input_row = this;
            var selectStates = $("select[name='state_id']");
            if ($("select[name='country_id']").length){
                selectStates.find("option:gt(0)").remove();
            }
            $(adv_input_row).on('change', "select[name='country_id']", function () {
                if ($("select[name='country_id']").val()) {
                    ajax.jsonRpc("/adv_signup/country_infos/" + $("select[name='country_id']").val(), 'call', {}).then(
                    function(data) {
                        if (data.states.length) {
                            selectStates.html('');
                            // selectStates.append($('<option>').text(' --Select-- '));
                            _.each(data.states, function(x) {
                                var opt = $('<option>').text(x[1])
                                    .attr('value', x[0]);
                                selectStates.append(opt);
                            });
                            selectStates.parent('div').show();
                        }
                        else {
                            selectStates.val('').parent('div').hide();
                            selectStates.removeAttr("required");
                        }
                    }
                    );
                }
            });
            $("select[name='country_id']").change();
        });
    });
});
