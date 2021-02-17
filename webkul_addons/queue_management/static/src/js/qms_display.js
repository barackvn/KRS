odoo.define('queue_management.qms_display', function (require) {
"use strict";

    var core = require('web.core');
    var ajax = require('web.ajax');

    var myVar;
    function showQueueStatus() {
        var offset = parseInt(document.getElementById('dept_offset').value);
        console.log(offset);
        ajax.jsonRpc("/counter/status/", 'call', { 'offset': offset})
            .then(function (vals) {
                var deptDiv = vals['deptDiv'];
                var moreRec = vals['more'];
                var resetValue = vals['reset'];
                var newOffset = vals['offset'];
                if (moreRec) {
                    var counterBody = $('.dept_div');
                    counterBody.replaceWith(deptDiv);
                    document.getElementById('dept_offset').value = parseInt(newOffset) + 1;
                } else if (resetValue) {
                    document.getElementById('dept_offset').value = 0;
                }
            });
        myVar = setTimeout(showQueueStatus, 7000);
    }
    
    $(document).ready(function() {

        showQueueStatus();

        function requestFullScreen(element) {
            // Supports most browsers and their versions.
            var requestMethod = element.requestFullScreen || element.webkitRequestFullScreen || 
                element.mozRequestFullScreen || element.msRequestFullScreen;
            var isInFullScreen = (document.fullscreenElement && document.fullscreenElement !== null) ||
                (document.webkitFullscreenElement && document.webkitFullscreenElement !== null) ||
                (document.mozFullScreenElement && document.mozFullScreenElement !== null) ||
                (document.msFullscreenElement && document.msFullscreenElement !== null);

            var docElm = document.documentElement;
            if (!isInFullScreen) {
                if (docElm.requestFullscreen) {
                    docElm.requestFullscreen();
                } else if (docElm.mozRequestFullScreen) {
                    docElm.mozRequestFullScreen();
                } else if (docElm.webkitRequestFullScreen) {
                    docElm.webkitRequestFullScreen();
                } else if (docElm.msRequestFullscreen) {
                    docElm.msRequestFullscreen();
                }
                var enter = document.getElementById('qms_enter');
                enter.style.display = 'none';
                var leave = document.getElementById('qms_leave');
                leave.style.display = 'initial';
                var close = document.getElementById('qms_close');
                if(close && close.style)
                    close.style.display = 'none';
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                } else if (document.mozCancelFullScreen) {
                    document.mozCancelFullScreen();
                } else if (document.msExitFullscreen) {
                    document.msExitFullscreen();
                }
                var enter = document.getElementById('qms_enter');
                enter.style.display = 'initial'; 
                var leave = document.getElementById('qms_leave');
                leave.style.display = 'none';
                var close = document.getElementById('qms_close');
                if(close && close.style)
                    close.style.display = 'initial';
            }
        }
        $('.qms_fs').on('click', function () {
            console.log('FullScreen');
            var elem = document.body; // Make the body go full screen.
            requestFullScreen(elem);
        });
    })



});
