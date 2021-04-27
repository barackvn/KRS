// openerp.kanak_appointment = function(instance) {
//     var _t = instance.web._t,
//         _lt = instance.web._lt,
//         QWeb = instance.web.qweb;

//     instance.web.views.add('calendar',
//         'instance.web_calendar.CalendarViewKanak');
//     instance.web_calendar.CalendarViewKanak = instance.web_calendar.CalendarView
//         .extend({
//             get_color: function(key) {
//                 if (this.name = 'Exception Calendar')
//                     if (this.color_map[key]) {
//                         return this.color_map[key];
//                     }
//                 var index = (((_.keys(this.color_map).length + 1) *
//                     5) % 24) + 1;
//                 if (key == 'appointment') {
//                     index = 'green';
//                 } else if (key == 'exception') {
//                     index = 'red';
//                 }
//                 this.color_map[key] = index
//                 return index;
//             },

//         })

// }
