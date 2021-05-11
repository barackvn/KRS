$(document).ready(function() {
    $('.appointment_timezone').on('change', function() {
        $('.appointment_form').submit();
    });
    $('.carousel').carousel('pause');
    var offset = -(new Date().getTimezoneOffset());
    var browser_offset = (offset < 0) ? "-" : "+";
    browser_offset += _.str.sprintf("%02d", Math.abs(offset / 60));
    browser_offset += _.str.sprintf("%02d", Math.abs(offset % 60));
    if (!$('.default_timezone').length) {
        $('.appointment_timezone option[data="' + browser_offset + '"]')
            .prop('selected', true);
        $('.appointment_form').submit();
    }
    var datepickers_options = {
        calendarWeeks: true,
        icons: {
            time: 'fa fa-clock-o',
            date: 'fa fa-calendar',
            up: 'fa fa-chevron-up',
            down: 'fa fa-chevron-down'
        },
        pickTime: false,
        defaultDate: new Date(),
    }
    var min_date = $('#jump_min_date').val();
    var max_date = $('#jump_max_date').val();
    if (min_date && max_date) {
        datepickers_options['minDate'] = new Date(min_date)
        datepickers_options['maxDate'] = new Date(max_date)
        datepickers_options['defaultDate'] = new Date(min_date)
    }
    $('.jump_to_date').datetimepicker(datepickers_options).on(
        'dp.change',
        function(e) {
            $('.appointment_form').submit();
        });
});


function populate_data(el){

    var country_id;
    country_id = $(el).val();
    console.log(">>>>>>>>>>country_id>>>>>>>>>>>",country_id);

        $.ajax({
            type: "POST",
            url: "/populate/data",
            data: {country_id:country_id},
        })
        .done(function(data){
             var load_data = jQuery.parseJSON(data);
             document.getElementById('dial_code').innerHTML="";



             if (load_data !== 'undifined' || load_data.length>0) {
//               var product_data="<option value=''>Select Product</option>"

//               console.log(">>>>>>>>>>>>product_data>>>>>>>>>",product_data);
//               ='<select name="product_id">'
                for(var i=0; i<load_data.length;i++){

                    dial_code ='<option value="'+load_data[i].country_id+'">'+load_data[i].dial_code+'</option>'
                    console.log(">>>>>>>>>>dial_code>>>>>>>>>>>",dial_code);


                }
//                product_data+='</select>'
//                   var product=document.getElementById("product")
                    var product=$('.dial_code');
                   console.log(">>>>>>>>>>>>>product",product);
                  $('.dial_code').append(dial_code);

             }

        });

};
