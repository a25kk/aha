requirejs(['require',
        '/scripts/flickity.pkgd.js',
        '/scripts/fontfaceobserver.js',
        '/scripts/hideShowPassword.js',
        '/scripts/jvfloat.js',
        '/scripts/respimage.js',
        '/scripts/ls.parent-fit.js',
        '/scripts/lazysizes-umd.js',
        '/scripts/a25.js',
        '/scripts/a25.helpers.js',
        '/scripts/a25.navbar.js'
    ],
    function(require, Flickity) {
        'use strict';

        if (typeof a25 == 'undefined') {
            var a25 = {};
        }


        // Trigger font face observer protection
        var fontPrimary = new FontFaceObserver('FFDINWebProLight', {
            weight: 400
        });
        var fontSecondary = new FontFaceObserver('FFDINWebProBold');

        fontPrimary.load(null, 3000).then(function () {
            document.documentElement.className += " font__primary--loaded";
        });

        fontSecondary.load(null, 3000).then(function () {
            document.documentElement.className += " font__secondary--loaded";
        });

        Promise.all([fontPrimary.load(null, 3000),
            fontSecondary.load(null, 3000)
        ])
            .then(function () {
                document.documentElement.className += " fonts--loaded";
            });

        if (navigator.userAgent.match(/iPhone|iPad|iPod/i)) {
            document.documentElement.className += " u-device--ios";
        };

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
        var $galleryContainer = document.querySelector('.main-gallery');
        if ($galleryContainer !== null) {
            var flkty = new Flickity('.main-gallery', {
                autoPlay: true,
                contain: true,
                wrapAround: true,
                imagesLoaded: true,
                cellSelector: '.app-gallery-cell',
                cellAlign: 'left',
                selectedAttraction: 0.025,
                friction: 0.28
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

        // Initialize scripts

        // Load Slider Resize
        window.addEventListener('load', function() {
            var sliders = Array.prototype.slice.call(document.querySelectorAll('.js-slider-resize'));
            if (sliders) {
                sliders.forEach(function(slider) {
                    var flkty = Flickity.data(slider);
                    flkty.resize()
                });
            }
        });



    });
