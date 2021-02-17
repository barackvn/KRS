/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */

odoo.define('marketplace_seller_blogs.marketplace_seller_blogs', function(require) {
    "use strict";
    var ajax = require('web.ajax');

    $(document).ready(function(){

        function shareArticle(event){
            var url = '';
            var blog_post = $(this).parents("[name='blog_post']");
            var blog_post_title = blog_post.find('.o_blog_post_title').html() || '';
            var blog_article_link = blog_post.find('.o_blog_post_title').parent('a').attr('href');
            if ($(this).hasClass('o_twitter')) {
                url = 'https://twitter.com/intent/tweet?tw_p=tweetbutton&text=Amazing blog article : '+blog_post_title+"! "+window.location.host+blog_article_link;
            } else if ($(this).hasClass('o_facebook')){
                url = 'https://www.facebook.com/sharer/sharer.php?u='+window.location.host+blog_article_link;
            } else if ($(this).hasClass('o_linkedin')){
                url = 'https://www.linkedin.com/shareArticle?mini=true&url='+window.location.host+blog_article_link+'&title='+blog_post_title;
            } else if ($(this).hasClass('o_google')){
                url = 'https://plus.google.com/share?url='+window.location.host+blog_article_link;
            }
            window.open(url, "", "menubar=no, width=500, height=400");
        }

        function mp_blog_post_snippet_load() {
            var mp_blog_post_snippet = document.getElementById('mp_blog_post_snippet');
            if (mp_blog_post_snippet != null) {
                $('.mp_blog_post_snippet').each(function(){
                    var $blog_div = $(this);
                        ajax.jsonRpc("/blog/snippet/load", 'call',{
                        })
                        .then(function (data) {
                            var $data = $(data);
                            $blog_div.replaceWith($data);
                        });
                });
            }
        }
        $('.o_twitter, .o_facebook, .o_linkedin, .o_google').on('click', shareArticle);
        mp_blog_post_snippet_load()
    });

});
