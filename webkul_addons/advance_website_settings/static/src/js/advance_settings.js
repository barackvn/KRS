odoo.define('advance_website_settings.advance_website_settings', function (require) {
"use strict";

    var core = require('web.core');
    var ajax = require('web.ajax');
    var _t = core._t;

    $(document).ready(function(){
      function escapeRegExp(text) {
        return text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&');
      }
      var code = $('html').attr('lang');
      var constraints;
      $('.oe_website_sale').find('.wk_cart_values').hide()

      try {
        ajax.jsonRpc('/website/wk_lang','call',{
          'code': code
        })
        .then(function(res){
         
          constraints=res;
        });

      } catch (e) {
        console.error(e);
      }

        $('.oe_website_sale').on('click', 'a[href$="/shop/checkout?express=1"]', function (ev)
        {   
          var conf_value = $('.oe_website_sale').find('.wk_cart_values span.oe_currency_value').slice(0,1).text();
          var cart_value = $('#order_total span.oe_currency_value').text();
          var thousand_sep = new RegExp(escapeRegExp(constraints.thousands_sep),"g")
          var decimal_sep = new RegExp(escapeRegExp(constraints.decimal_point),"g")
          var cart=parseFloat(cart_value.replace(thousand_sep,'').replace(decimal_sep,'.'))
          var check=parseFloat(conf_value.replace(thousand_sep,'').replace(decimal_sep,'.'))
          var currency_symbol = $('.oe_website_sale').find('.wk_cart_values').attr('currency_symbol');
          var $link = $(this);
            if (cart<check)
            {
                ev.preventDefault();
                $(this).popover({
               
                  title: _t("WARNING!!"),
                  placement:"top",
                  trigger:'focus',
                });
                $(this).attr('data-content',_t("A minimum purchase total of ")+ currency_symbol+" "+ conf_value+_t(" is required to validate your order, current purchase total is ")+ currency_symbol+" "+ cart_value);
                $(this).popover('show');

            }
            setTimeout(function() {$link.popover("dispose");},3000);
        });

       var totalPriceElem = $('#sub_total span');
       var quantityField = $('.css_quantity input[type="text"].quantity');
       var defaultPrice = $('.oe_price_h4 b.oe_price .oe_currency_value');
       var price;

       function numberWithCommas(x,dec_point,thousands_sep,grouping) {
         //[3,3],,,[3,0],,,[] => three cases are there for now in odoo
         //Implemented for speciific these cases

         var parts = x.toString().split(dec_point);
         grouping = grouping.slice(1,grouping.length-1); // grouping == string, sliced '[' & ']'

         if(grouping.length == 0) {
           parts[0] = parts[0].replace(/\B(?=(\d{0})+(?!\d))/g, thousands_sep);
         }
         else if (grouping.length == 3 && grouping[0] == '3'  && grouping[2] == '0') {
           parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, thousands_sep);
         }
         else {
           let len = parts[0].length;
           if(len <= 3) {}
           else if(len <= 6 && len >= 4) {
             let part_last = parts[0].slice(-3);
             parts[0] = parts[0].slice(0,len-3) + thousands_sep + part_last;
           }
           else if(len > 6) {
             let part_last_1 = parts[0].slice(-3);
             let part_last_2 = parts[0].slice(-6,-3);
             parts[0] = parts[0].slice(0,len-6) + thousands_sep + part_last_2 + thousands_sep + part_last_1;
           }
           else {}
         }
          return parts.join(dec_point);
        }

       
       defaultPrice.on('DOMSubtreeModified',function(){
          try {
            ajax.jsonRpc('/website/wk_lang','call',{
              'code': code
            })
            .then(function(res){
              const dec_point = res.decimal_point;
              const thousands_sep = res.thousands_sep;
              const grouping = res.sep_format;

              if(dec_point == '.') {
                price = defaultPrice.text().split(thousands_sep).join('');
                totalPriceElem.text(numberWithCommas((quantityField.val()*price).toFixed(2),dec_point,thousands_sep,grouping));
              }
              else if(dec_point == ',') {
                price = defaultPrice.text().split(thousands_sep).join('');
                price = price.replace(',','.');
                price = (quantityField.val()*price).toFixed(2);
                price = price.replace('.',',');
                totalPriceElem.text(numberWithCommas(price,dec_point,thousands_sep,grouping));
              }
            });

          } catch (e) {
            console.error(e);
          }
        });
    });
});
