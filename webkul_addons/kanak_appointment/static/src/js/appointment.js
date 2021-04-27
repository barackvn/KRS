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
