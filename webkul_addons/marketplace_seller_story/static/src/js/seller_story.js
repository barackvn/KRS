odoo.define('marketplace_seller_badges.seller_badges', function (require) {
    "use strict";

    $(document).ready(function () {
        $('.mp_story_owl-carousel').owlCarousel({
            items: 3,
            navigation: true,
            pagination: false,
            slideSpeed: 500,
            autoPlay: false,
            stopOnHover: true,
            navigationText: []
        });
        function copyToClipboard(element) {
            var $temp = $("&lt;input&gt;");
            $("body").append($temp);
            $temp.val($(element).text()).select();
            document.execCommand("copy");
            $temp.remove();
        }
    });

    $(document).on('click', ".video-play", function (event) {
        var story_video_modal_id = $(this).attr('id');
        var url = 'https://www.youtube.com/embed/' + story_video_modal_id;
        url = url + "?autoplay=1"
        var seller_video_modal = '<div id="wk_ss_v_modal" class="modal fade seller-story-modal" role="dialog">\
                            <div class="modal-dialog modal-lg">\
                                <div class="">\
                                    <button type="button" class="close fa fa-times wk_closed_btn" data-dismiss="modal"/>\
                                    <div class="seller-story-iframe-div" style="text-align: center;">\
                                        <iframe class="seller-story-iframe" id="video_tutorial" type="text/html" style="height: 347px;width: 841px;" frameborder="0" allowfullscreen="" src=' + url + '></iframe>\
                                    </div>\
                                </div>\
                            </div>\
                        </div>'
        $(seller_video_modal).appendTo('body');
        $("#wk_ss_v_modal").modal('show');
        $("#wk_ss_v_modal").on("hidden.bs.modal", function () {
            $(this).remove();
        });
    });
        
});