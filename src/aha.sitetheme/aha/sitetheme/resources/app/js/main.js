'use strict';
(function ($) {
    $(document).ready(function () {
        // Toogle gallery caption display
        var $captionToggle = $('.js-caption-collapsible'),
            $captionToggleTitle = $('.js-toggleable-title'),
            $toggleableSection = $('.js-toggleable'),
            $toggleOpenClass = 'toggleable-open',
            $collapsingElement = $('#app-gallery-caption-block');
        $captionToggle.on('click', function(event) {
            event.preventDefault();
            if($toggleableSection.hasClass($toggleOpenClass)) {
                $collapsingElement.removeClass('fadeInDown')
                    .addClass('fadeOutUp');
                $captionToggleTitle.removeClass('fadeOut').addClass('fadeIn');
                $toggleableSection.delay(1000).queue(function (next) {
                    $(this).removeClass($toggleOpenClass);
                    next();
                });
            } else {
                $collapsingElement.removeClass('fadeOutUp').addClass('fadeInDown');
                $captionToggleTitle.removeClass('fadeIn').addClass('fadeOut');
                $toggleableSection.delay(1000).queue(function (next) {
                    $(this).addClass($toggleOpenClass);
                    next();
                });
            }
        });
        // Initialize flickity galleries
        var $galleryContainer = $('.main-gallery');
        if ($galleryContainer) {
            var flkty = new Flickity('.main-gallery', {
                autoPlay: true,
                contain: true,
                wrapAround: true,
                imagesLoaded: true,
                cellSelector: '.app-gallery-cell',
                cellAlign: 'left'
            });
            // Trigger flickity gallery transitions via thumbnail anchors
            $('.js-thumbtrigger').each( function() {
                $(this).on('click', function (evt) {
                    evt.preventDefault();
                    var index = $(this).data('index');
                    $(this).toggleClass('js-thumbtrigger-active');
                    flkty.select(index);
                });
            });
        }
        if ($(".userrole-anonymous")[0]) {
            $('input[type="password"]').showPassword('focus', {});
            $('.app-signin-input').jvFloat();
            var $mcNote = $('#app-signin-suggestion');
            Mailcheck.defaultDomains.push('aha.kreativkombinat.de')
            $('[data-appui="mailcheck"]').on('blur', function (event) {
                $(this).mailcheck({
                    // domains: domains,                       // optional
                    // topLevelDomains: topLevelDomains,       // optional
                    suggested: function (element, suggestion) {
                        // callback code
                        $mcNote.removeClass('hidden').addClass('fadeInDown');
                        $mcNote.html("Meinten Sie <i>" + suggestion.full + "</i>?");
                        $mcNote.on('click', function (evt) {
                            evt.preventDefault();
                            $('#ac-name').val(suggestion.full);
                            $mcNote.removeClass('fadeInDown').addClass('fadeOutUp').delay(2000).addClass('hidden');
                        });
                    },
                    empty: function (element) {
                        // callback code
                        $mcNote.html('').addClass('hidden');
                    }
                });
            });
        }
    });
}(jQuery));
