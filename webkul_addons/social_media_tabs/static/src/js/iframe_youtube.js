odoo.define('social_media_tabs.youtube_iframe', function (require) {
    "use strict";

    var ajax = require('web.ajax');
    var sAnimation = require('website.content.snippets.animation');

    sAnimation.registry.youtubeIFrame = sAnimation.Class.extend({
        selector: "li[data-tab_name='youtube']",
        read_events: {
            'click  a': '_render_frame',
            'click .wk_close_frame': '_close_frame',
        },
        getId: function(url) {
            var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
            var match = url.match(regExp);
            if (match && match[2].length == 11) {
                return match[2];
            } else {
                return false;
            }
        },
        _render_frame: function(evt) {
            evt.preventDefault();
            evt.stopPropagation();
            let $youtubeChannelFrame = $('.youtube_frame_video');
            let href = $(evt.currentTarget).attr('href');
            let id = this.getId(href);
            if(id != 0) {
                $youtubeChannelFrame.addClass('active');
                href = `//www.youtube.com/embed/${id}`;
                var customFrame = '<iframe class="youtube_video_iframe" src='+ href +' width="100%" height="100%" frameborder="0" webkitallowfullscreen="" mozallowfullscreen="" allowfullscreen=""></iframe><i class="wk_close_frame fa fa-times"></i>';
                $youtubeChannelFrame.append(customFrame).show();
                // $('.wk_close_frame').mouseenter(function() {
                //     console.log(color);
                //     $(this).css('background-color', color);
                // });
            } else {
                console.log('Invalid youtube video ID');
            }
        },
        _close_frame: function(evt) {
            evt.stopPropagation();
            $('.youtube_frame_video').empty().removeClass('active');
        },
    });
});
