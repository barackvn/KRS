odoo.define('queue_management.main', function (require) {
"use strict";

    var core = require('web.core');
    var ajax = require('web.ajax');
    var Session = require('web.Session');
    var QWeb = core.qweb;
    var _t = core._t;
    
    $(document).ready(function() {

        $('#list_refr').on('click', function () {
            var offset = document.getElementById('list_refr').value;
            var qsession = document.getElementById('q_session').value;
            var newOffset = parseInt(offset) * 7;
            ajax.jsonRpc("/today/tokens/", 'call', { 'offset': newOffset, 'session': qsession })
                .then(function (vals) {
                    var tbody = vals['tbody'];
                    var moreRec = vals['more'];
                    if (moreRec) {
                        var tkBody = $('#token_body');
                        tkBody.replaceWith(tbody);
                    }
                });
        });

        $('#list_left').on('click', function () {
            var offset = document.getElementById('list_left').value;
            var rightOffset = document.getElementById('list_right').value;
            var refOffset = document.getElementById('list_refr').value;
            var qsession = document.getElementById('q_session').value;
            var newOffset = parseInt(offset) * 7;
            if (newOffset >= 0) {
                ajax.jsonRpc("/today/tokens/", 'call', { 'offset': newOffset, 'session': qsession })
                    .then(function (vals) {
                        var tbody = vals['tbody'];
                        var moreRec = vals['more'];
                        if (moreRec) {
                            document.getElementById('list_refr').value = parseInt(refOffset) - 1;
                            document.getElementById('list_left').value = parseInt(offset) - 1;
                            document.getElementById('list_right').value = parseInt(rightOffset) - 1;
                            var tkBody = $('#token_body');
                            tkBody.replaceWith(tbody);
                        }
                });
            }
        });

        $('#list_right').on('click', function () {
            var offset = document.getElementById('list_right').value;
            var leftOffset = document.getElementById('list_left').value;
            var refOffset = document.getElementById('list_refr').value;
            var qsession = document.getElementById('q_session').value;
            var newOffset = parseInt(offset) * 7;
            ajax.jsonRpc("/today/tokens/", 'call', { 'offset': newOffset, 'session': qsession })
                .then(function (vals) {
                    var tbody = vals['tbody'];
                    var moreRec = vals['more'];
                    if (moreRec) {
                        document.getElementById('list_refr').value = parseInt(refOffset) + 1;
                        document.getElementById('list_right').value = parseInt(offset) + 1;
                        document.getElementById('list_left').value = parseInt(leftOffset) + 1;
                        var tkBody = $('#token_body');
                        tkBody.replaceWith(tbody);
                    }
            });
        });

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
            var elem = document.body; // Make the body go full screen.
            requestFullScreen(elem);
        });

        $('.print_token_pdf').on('click', function () {
            var tokenId = document.getElementById('token_id').value;
            var tokenSession = document.getElementById('session_id').value;
            var attachmentId = document.getElementById('attachment_id').value;
            var isPrinter = document.getElementById('is_printer').value;
            var token_nmbr = document.getElementById('token_nmbr').value;
            var comapny_name = document.getElementById('comapny_name').value;
            var ip_addr = document.getElementById('ip_addr').value;
            console.log('comapny_name', comapny_name);
            console.log('token_nmbr', token_nmbr);
            console.log('ip_addr', ip_addr);
            if (!ip_addr) {
                console.log('not ip_addr');
                var redirect = "/web/content/" + attachmentId + "/token_" + tokenId;
                window.location = redirect;
            } else {
                var url = 'http://' + ip_addr + ':8069';
                console.log('url ', url);
                this.connection = new Session(undefined,url, { use_cors: true});
                this.host       = url;
                self = this;
                var tmp_re = "<receipt align='center' width='50' value-thousands-separator='' >"
                tmp_re += "<h1>" + comapny_name + "</h1>" + "<br/><br/>"
                tmp_re += "<h1>" + 'Token' + "</h1>" + "<br/>"
                tmp_re += "<h1>" + token_nmbr + "</h1>" + "<br/><br/><br/>"
                tmp_re += "<div>" + moment().format("YYYY-MM-DD HH:mm:ss") + "</div>" + "<br/>"
                tmp_re += "<div>" + '-----------------------------' + "</div>" + "<br/>"
                tmp_re += "<div font='b' line-ratio='1.0'><line><left>"
                tmp_re += 'Please take your seat, we will attain you soon!!'
                tmp_re += "</left></line></div>"
                tmp_re += "</receipt>";
                self.connection.rpc('/hw_proxy/print_xml_receipt',{receipt: tmp_re},{timeout: 5000})
                .then(function(){
                    console.log('Called');
                },function(error, event){
                    console.log('There was an error while trying to print the token:');
                    console.log(error);
                });
            }

            setTimeout(function () {
                console.log('timeout here');
                var redirect_url = "/qms/web/session/" + tokenSession;
                window.location = redirect_url;
            }, 1000);

        });

    })



});
