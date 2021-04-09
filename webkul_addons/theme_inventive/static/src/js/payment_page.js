odoo.define('theme_inventive.payment_form', function(require) {
    "use strict";
    var publicWidget = require('web.public.widget');
    var payment_form = require('payment.payment_form');
    var PaymentForm = publicWidget.registry.PaymentForm;

    publicWidget.registry.PaymentForm = PaymentForm.extend({
        updateNewPaymentDisplayStatus: function() {
            var checked_radio = this.$('input[type="radio"]:checked');
           // we hide all the acquirers form
           this.$('[id*="o_payment_add_token_acq_"]').addClass('d-none');
           this.$('[id*="o_payment_form_acq_"]').addClass('d-none');
           if (checked_radio.length !== 1) {
               return;
           }
           checked_radio = checked_radio[0];
           var acquirer_id = this.getAcquirerIdFromRadio(checked_radio);

           // if we clicked on an add new payment radio, display its form
           if (this.isNewPaymentRadio(checked_radio)) {
               this.$('#o_payment_add_token_acq_' + acquirer_id).removeClass('d-none');
           }
           else if (this.isFormPaymentRadio(checked_radio)) {
               this.$('#o_payment_form_acq_' + acquirer_id).removeClass('d-none');
           }
            // custom code .........................................
            var $checked_radio = this.$('input[type="radio"]:checked');
            let $card = $checked_radio.parents(".card").find(".card-body label").removeClass("active");
             $checked_radio.parent().addClass("active");
            // custom code ends.................................

        },
    });
    return PaymentForm
});
