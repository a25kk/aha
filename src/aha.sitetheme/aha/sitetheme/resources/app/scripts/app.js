requirejs(['require',
        '/scripts/flickity.pkgd.js',
        '/scripts/fontfaceobserver.js',
        '/scripts/hideShowPassword.js',
        '/scripts/jvfloat.js',
        '/scripts/respimage.js',
        '/scripts/ls.parent-fit.js',
        '/scripts/lazysizes-umd.js',
        '/scripts/a25.js',
        '/scripts/a25.helpers.js'
    ],
    function(require, Flickity) {
        'use strict';

        // Trigger font face observer protection
        // Trigger font face observer protection
        var fontPrimary = new FontFaceObserver('FFDINWebProBold');
        var fontSecondary = new FontFaceObserver('FFDINWebProLight');

        fontPrimary.load().then(function () {
            document.documentElement.className += " font__primary--loaded";
        });

        fontSecondary.load().then(function () {
            document.documentElement.className += " font__secondary--loaded";
        });

        Promise.all([fontPrimary.load(), fontSecondary.load()]).then(function () {
            document.documentElement.className += " fonts--loaded";
        });

        var $galleryContainer = document.querySelector('.main-gallery');
        // Content image galleries
        if ($galleryContainer !== null) {
            var flkty = new Flickity('.main-gallery', {
                autoPlay: true,
                contain: true,
                wrapAround: true,
                imagesLoaded: true,
                cellSelector: '.app-gallery-cell',
                cellAlign: 'left'
            });
            $galleryContainer.classList.add('app-banner--loaded');
            // Trigger gallery transitions via thumbnail anchors
            var thumbnailTrigger = Array.prototype.slice.call(document.querySelectorAll('.js-thumbtrigger'));
            if (thumbnailTrigger) {
                thumbnailTrigger.forEach(function(element, index) {
                    element.addEventListener('click', function(event) {
                        event.preventDefault();
                        var index = element.getAttribute('data-index');
                        element.classList.toggle('js-thumbtrigger-active');
                        flkty.select(index);
                    }, false);
                });
            }
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
    }
)
