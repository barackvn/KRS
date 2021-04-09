/* Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
odoo.define('social_media_tabs.social_media_tabs', function (require) {
    "use strict";

    $(document).ready(function() {
        $('main').click(function() {
            $('.js_fetch_data').removeClass('active');
            $('.js_social_data').removeClass('active');
        });
    })

    var ajax = require('web.ajax');
    var sAnimation = require('website.content.snippets.animation');

    sAnimation.registry.social_media_tabs = sAnimation.Class.extend({
        selector: '#social_media_tabs',
        read_events: {
            'click .js_fetch_data': '_render_social_tab',
            'click .js_social_data': '_prevent',
            'mouseenter .js_render_tabs.js_hover': '_render_tabs',
            'click .js_render_tabs.js_click': '_hybrid_render_tabs',
            'click .js_disable_tab': '_hybrid_disable_tabs',
            //for vimeo player
            'click .vimeo': '_render_vimeo_video',
            'click .vimeo_remove': '_disable_frame',
        },
        _set_data: function($target, response, tab_name, res) {
            var html = '';
            var error = '<p class="text-danger">Looks like something went wrong!!!</p>'
            var items;
            var limit = res.limit;
            switch(tab_name) {
                case 'youtube':
                    items = response.items;
                    if ( items ) {
                        $target.find('.loader').remove();
                        $.each(items, function (i, item){
                            html += '<div class="d-flex feed y_feeds pt8 pb8"><a class="mr16 img" href = http://www.youtube.com/watch?v=' + item.id.videoId + '><img src = '+ item.snippet.thumbnails.default.url +'></img></a><div><a class="title" href = http://www.youtube.com/watch?v=' + item.id.videoId + '>'+ item.snippet.title +'"</a><p>'+ item.snippet.description +'</p></div></div>';
                        })
                    } else {
                        html = response.error;
                    }
                    $target.html(html);
                    $target.append('<div class="d-none youtube_frame_video"/>');
                    if ( res.subscribe[0] == true ) {
                        $target.append('<div class="y_subscribe"><script src="https://apis.google.com/js/platform.js"></script><div class="g-ytsubscribe" data-channelid="'+ res.channel_id[0] +'"></div></div>');
                    }

                    break;
                case 'tumblr':
                    items = response.posts;
                    let count = 0;
                    if ( items.length ) {
                        $target.find('.loader').remove();
                        $.each(items, function (i, item) {
                            let anchor = item['url-with-slug'];
                            let title;
                            let body;
                            // let like_button = item['like-button'];
                            switch( item.type ) {
                                case 'regular':
                                    title = item['regular-title'];
                                    body = item['regular-body'];
                                    html = '<div class="tumbler_items feed regular"><a href="'+ anchor +'">'+ title +'</a>'+ body +'</div>';
                                    break;
                                case 'photo':
                                    title = item['photo-caption'];
                                    body = item['photo-url-75'];
                                    html = '<div class="tumbler_items feed photo"><a href="'+ anchor +'"><img src="'+ body +'"></img></a>'+ title + '<div class="mt16" style="flex: 100%"></div></div>';
                                    break;
                                case 'quote':
                                    title = item['quote-text'];
                                    body = item['quote-source'];
                                    html = '<div class="tumbler_items feed quote"><a href="'+ anchor +'">'+ title +'</a><p>'+ body +'</p></div>';
                                    break;
                                case 'link':
                                    title = item['link-text'];
                                    body = '<a href="' + item['link-url'] + '">'+ item['link-url'] +'</a>';
                                    let description = item['link-description'];
                                    html = '<div class="tumbler_items feed link"><a href="'+ anchor +'">'+ title +'</a>'+ body +''+ description + '</div>';
                                    break;
                                case 'conversation':
                                    title = item['conversation-title'];
                                    body = item['conversation-text'];
                                    html = '<div class="tumbler_items feed conversation"><a href="'+ anchor +'">'+ title +'</a>'+ body + '</div>';
                                    break;
                                case 'video':
                                    title = item['video-caption'];
                                    body = o.video != '400' ? item['video-player-' + o.video] : item['video-player'];
                                    html = '<div class="tumbler_items feed video"><a href="'+ anchor +'">'+ title +'</a><p>'+ body +'</p></div>';
                                    break;
                                case 'audio':
                                    title = item['audio-caption'];
                                    body = item['audio-embed'];
                                    let audio_title = item['id3-title'];
                                    html = '<div class="tumbler_items feed audio"><a href="'+ anchor +'">'+ audio_title +'</a>'+ title + '' + body + '</div>';
                                    break;
                            }
                            $target.append(html);
                            if ( count == limit ) {
                                return False
                            }
                            count ++;
                        })
                    } else {
                        $target.append(error);
                    }
                    break;
            }
        },
        _getFeed: function($target, tab_name, url, data, res, cache, dataType) {
            var self = this;
            $.ajax({
                url: url,
                data: data,
                cache: cache,
                dataType: dataType,
                success: function (response) {
                    self._set_data($target, response, tab_name, res);
                }
            })
        },
        _data: function(tab_id, $target) {
            var self = this;
            let loader = `<div class="loader">
                            <span></span>
                            <span></span>
                        </div>`;
            $target.append(loader);
            ajax.jsonRpc(
                '/socialTabs/url','call', {
                    'tab_id': tab_id
                })
            .then(function(res) {
                let html = '';
                var limit = res.limit
                let count = 0;
                var tab_type = res.type;
                var social_tab = res.social_tab;
                var data = 'https://ajax.googleapis.com/ajax/services/feed/load?v=1.0';
                if (tab_type == 'social_tab') {
                    switch (social_tab) {
                        case "facebook":
                            // Plugin for facebook
                            var fb_id = res.fb_id;
                            html = '<div id="fb-root"></div> <script async defer crossorigin="anonymous" src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v5.0"></script> <div class="fb-page"    data-href="https://www.facebook.com/' + fb_id + '" data-tabs="timeline" data-height="400" data-width="400" data-small-header="false" data-adapt-container-width="true" data-hide-cover="false" data-show-facepile="true"> </div>';
                            // Prevent facebook js to load multiple times as it will cause issue
                            if ( $target.find('#fb-root').length == 0 ) {
                                $target.html(html);
                            }
                            $target.find('.loader').remove();
                            break;
                        case 'twitter':
                            // Plugin for Twitter
                            var twitter_id = res.twiter_user_id[0];
                            var href = "https://twitter.com/" + twitter_id;
                            $target.html('<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>  <a class="twitter-timeline" href = "' + href + '"/>');
                            $target.find('.loader').remove();
                            break;
                        case 'youtube':
                            var id = res.user_id;
                            var channel_id = res.channel_id;
                            var apikey = res.api_key;
                            var url = 'https://www.googleapis.com/youtube/v3/search?key=' + apikey + '&channelId=' + channel_id + '&part=snippet&maxResults=' + res.limit + '';
                            self._getFeed($target, 'youtube', url, data, res, true, 'json');
                            break;
                        case 'tumblr':
                            // Old API (v1)
                            var id = res.tumblr_id[0];
                            url = 'https://' + id + '.tumblr.com/api/read/json?callback=?';
                            self._getFeed($target, 'tumblr', url, data, res, true, 'json');
                            break;
                        case 'pinterest':
                            var id = res.pinterest_id[0];
                            html = `<script type="text/javascript" async defer src="//assets.pinterest.com/js/pinit.js"></script>
                            <a href="https://www.pinterest.com/${id}/"
                                data-pin-do="embedUser"
                                data-pin-board-width="400"
                                data-pin-scale-height="320"
                                data-pin-scale-width="80">
                            </a>`
                            $target.find('.loader').remove();
                            $target.html(html);
                            break;
                        case 'vimeo':
                            let name = '';
                            let description = '';
                            count = 0;
                            if (res.vimeo_data.data) {
                                $target.find('.loader').remove();
                                $.each(res.vimeo_data.data, function(i, data) {
                                    name = data.name ? data.name : 'This video has no name';
                                    description = data.description ? data.description : 'This video has no description';
    
                                    html = '<div class="d-flex vimeo feed pt16 pb16">'+ data.embed.html +'<div class="video_details"><div class="name"><a href="'+ data.link +'"><p>'+ name +'</p></a></div><div class="description"><p>'+ description +'</p></div><div class="duration">'+ data.duration/60 + 'min' + '</div></div>';
                                    $target.append(html);
                                    if ( count == limit ) {
                                        return False
                                    }
                                    count ++;
                                });
                            }
                            break;
                        case 'instagram':
                            if ( res.instagram_data ) {
                                count = 1;
                                if (res.instagram_data) {
                                    $target.find('.loader').remove();
                                    $.each(res.instagram_data, function(i, data) {
                                        let caption;
                                        caption = data.hasOwnProperty('caption') ? data.caption : '';
                                        let media_type = data.media_type;
                                        let media_url = data.media_url;
                                        let timestamp = data.timestamp;
        
                                        html = '<div class="d-flex flex-wrap instagram feed pt16 pb16"><div class="media"><a href="'+ media_url +'"><img src="'+ media_url +'"></img></a></div><div class="caption mt16 py-1">'+ caption +'<span></span></div></div>';
                                        $target.append(html);
                                        
                                        if ( count == limit ) {
                                            return False
                                        } 
                                        count ++;
                                    });
                                }
                            }
                            break;
                        case 'flickr':
                            // In case of flickr we are getting CROS issue, hence this is done through python
                            let flickr_data = res.flickr_data;
                            count = 1;
                            if (flickr_data.items) {
                                $target.find('.loader').remove();
                                $.each(flickr_data.items, function(i, data) {
                                    let title = data.title;
                                    let media = data.media;
                                    let link = data.link;
                                    html = 
                                        `<div class="d-flex flex-wrap flickr feed pt16 pb16">
                                            <a href="${link}">
                                                <img class="img img-fluid" src="${media.m}"></img>
                                            </a>
                                            <div class="content_data">
                                                <h6>
                                                    <a href="${link}">
                                                        ${title}
                                                    </a>
                                                </h6>
                                            </div>
                                        </div>`;
                                        $target.append(html);
                                        if ( count == limit ) {
                                            return;
                                        }
                                        count ++;
                                })
                            }
                            break;
                    }
                } else {
                    $target.append(res.custom_html);
                }
                $target.find('.loader').remove();
            });
        },
        _render_social_tab: function(evt) {
            evt.stopPropagation();
            
            var self = this;

            let $target = $(evt.currentTarget);
            const $js_social_data = $target.find('.js_social_data');
            let $dataBody = $js_social_data.find('.body');
            if ( $js_social_data.attr('data-tab_name') != 'facebook') {
                $dataBody.empty();
            }

            if( $target.hasClass('active') ) {
                $target.removeClass('active')
                $js_social_data.removeClass('active');
                return;
            }

            $js_social_data.addClass('active');
            $js_social_data.find('.follow_button').css('background-color', $js_social_data.find('.js_social_follow').data('color'));

            let tab_id = $target.data('tab_id');
            let $active_tab = $target.closest('ul').find('li.active');
            $active_tab.removeClass('active').find('.js_social_data').removeClass('active');
            $target.addClass('active');

            // Call to get social tab related data from res.config
            self._data(tab_id, $dataBody);
        },
        _prevent: function(evt) {
            evt.stopPropagation();
        },
        _render_tabs: function(evt) {
            this._hybrid_render_tabs(evt);
        },
        _hybrid_render_tabs: function(evt) {
            let $target = $(evt.currentTarget);
            let $social_wrapper = $target.siblings('.social_wrapper');
            $target.css({'transform': 'translateX(-100%)', 'transition': 'transform .4s'});
            setTimeout(function() {
                $target.css('display', 'none');
                $social_wrapper.addClass('disabled');
                $social_wrapper.css({'display':'block', 'opacity': 0});
            }, 400);
            setTimeout(function() {
                $social_wrapper.removeClass('disabled');
                $social_wrapper.css({'transform': 'translateX(0)', 'opacity': '1', 'transition': 'all .4s'});
            }, 500);
        },
        _hybrid_disable_tabs: function(evt) {
            let $target = $(evt.currentTarget);
            let $social_wrapper = $target.closest('.social_wrapper');
            $social_wrapper.css({'transform': 'translateX(-100%)', 'opacity': '0', 'transition': 'all .4s'});
            setTimeout(function() {
                $social_wrapper.css('display', 'none');
                $social_wrapper.siblings('.js_render_tabs').addClass('disabled');
                $social_wrapper.siblings('.js_render_tabs').css({'display': 'block', 'opacity': '0'});
            }, 400);
            setTimeout(function() {
                $social_wrapper.siblings('.js_render_tabs').css({'transform': 'translateX(0)', 'opacity': '1', 'transition': 'all .4s'});
                $social_wrapper.siblings('.js_render_tabs').removeClass('disabled');
            }, 500);

        },
        _render_vimeo_video: function(evt) {
            let $vimeo = $(evt.currentTarget).closest('.vimeo');
            $vimeo.addClass('full').append('<div class="vimeo_remove"><i class="fa fa-window-close"></i></div>');
        },
        _disable_frame: function(evt) {
            evt.stopPropagation();
            let $currentTarget = $(evt.currentTarget);
            $currentTarget.closest('.vimeo').removeClass('full');
            $currentTarget.remove();
        }
    });
});
