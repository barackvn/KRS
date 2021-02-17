odoo.define('refer_and_earn.my',function(require){
"use strict";

var core = require('web.core');
var ajax = require('web.ajax');

var _t = core._t;

  $(document).ready(function() {
    google.charts.load("current", {packages:["corechart"]});
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {
      if($('#matrix').length){
        var mat = $('#matrix').val().split("-");
      // else
      //  var mat = 0;
      var data = google.visualization.arrayToDataTable([
        ['State', 'total state types'],
        ['Approved',  parseInt(mat[4])],
        ['Pending',     parseInt(mat[0])],
        ['Error',     parseInt(mat[1])],
        ['Rejected',  parseInt(mat[2])],
        ['Cancel',    parseInt(mat[3])],
        ['No Referral Stat',  parseInt(mat[5])],
      ]);
      var mat = $('#matrix').val().split("-");
      var options = {
        title:' ',
        pieHole: 0.4,
        colors : ['#337ab7','#ec971f','#3c763d','red','#b733ad','grey'],
      };
      var chart = new google.visualization.PieChart(document.getElementById('donutchart'));
      chart.draw(data, options);
    }
  }


  });







});
