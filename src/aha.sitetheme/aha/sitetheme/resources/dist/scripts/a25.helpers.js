if (typeof a25 == "undefined") var a25 = {};

a25.helpers = (function($, undefined) {
    "use strict";

    var _defaults = {
        anonymousUserClass: ".userrole-anonymous",
        passwordInput: "input[type=\"password\"]",
        toggleableCaptions: ".js-caption-collapsible"
    };

    function init(_options) {
        signUpFormHelpers(_options);
        togglableCaptions(_options);
    }

    function signUpFormHelpers(_options) {
        var options = $.extend({}, _defaults, _options);
        var $anonymousUser = document.querySelector(options.anonymousUserClass);
        if ($anonymousUser !== null) {
            var inputPassword = $(options.passwordInput);
            inputPassword.hideShowPassword(true, "focus");
        }
    }

    function togglableCaptions(_options) {
        // Toogle gallery caption display
        var options = $.extend({}, _defaults, _options);
        var $captionToggle = $(options.toggleableCaptions),
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
    }

    return {
        init: init
    };
})(jQuery);

jQuery(function() {
    a25.helpers.init();
});
