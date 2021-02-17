odoo.define('odoo_gdpr.custom',function(require){
"use strict";

    var core = require('web.core');
    var ajax = require('web.ajax');

    var _t = core._t;

    $(document).ready(function() {
         $('[data-toggle="tooltip"]').tooltip();
         $('.oe_cart').on('click', '.js_my_edit_address', function() {
            $(this).closest('div.one_kanban').find('form.d-none').attr('action', '/my/edit/address').submit();
        });

        $('.modalClose').on('click', function() {
            $('.modal-backdrop').remove();
            location.reload();

        });

        $('.download_submit_form').on('click',function(){
            var $form =$(this).closest('#download_form');
            var partner_id = $form.find("input[name='partner_id']").val();
            var operation_type = $form.find("input[name='operation_type']").val();
            var object_id = $form.find("input[name='object_id']").val();
            var action_type = $form.find("input[name='action_type']").val();
            var type = $form.find("input[name='type']").val();
            ajax.jsonRpc(
                 "/download/personal_data",
                 'call',{
                    'partner_id': partner_id,
                    "operation_type":operation_type,
                    "object_id":object_id,
                    "action_type":action_type,
                    "type":type

                  }).then(function (result){

                  if (result){
                    console.log(result);
                    $("#gdpr-request-popup").text(result.alert_msg);
                    $("#myModalalert").modal('show');
                  }
                  else{

                  }
              });
            return false;
         });

        $('.delete_submit_form').on('click',function(){
            var $form =$(this).closest('#delete_form');
            var partner_id = $form.find("input[name='partner_id']").val();
            var operation_type = $form.find("input[name='operation_type']").val();
            var object_id = $form.find("input[name='object_id']").val();
            var action_type = $form.find("input[name='action_type']").val();
            var type = $form.find("input[name='type']").val();
            ajax.jsonRpc(
                 "/delete/personal_data",
                 'call',{
                    'partner_id': partner_id,
                    "operation_type":operation_type,
                    "object_id":object_id,
                    "action_type":action_type,
                    "type":type

                  }).then(function (result){
                  if (result){
                    console.log(result);
                    $("#gdpr-request-popup").text(result.alert_msg);
                    $('#myModal').hide();
                    $("#myModalalert").modal('show');
                  }
                  else{

                  }
              });


            return false;
        });

        $('#delete_form').on('submit',function(e){
            e.preventDefault();
            var $form =$(this).closest('#delete_form');
            var partner_id = $form.find("input[name='partner_id']").val();
            var operation_type = $form.find("input[name='operation_type']").val();
            var object_id = $form.find("input[name='object_id']").val();
            var action_type = $form.find("input[name='action_type']").val();
            var type = $form.find("input[name='type']").val();
            if ($('input[type=checkbox]').prop('checked')){
                console.log("checked")
            ajax.jsonRpc(
                 "/delete/personal_data",
                 'call',{
                    'partner_id': partner_id,
                    "operation_type":operation_type,
                    "object_id":object_id,
                    "action_type":action_type,
                    "type":type

                  }).then(function (result){
                  if (result){
                    console.log(result);
                    $("#gdpr-request-popup").text(result.alert_msg);
                    $('#myModal').hide();
                    $("#myModalalert").modal('show');
                  }
                  else{

                  }
              });
            }
            else{
                console.log("unchecked")
            }
            return false;
        });

    });



});
