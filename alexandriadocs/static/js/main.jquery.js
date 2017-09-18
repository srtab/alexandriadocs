/* globals jQuery */
"use strict";

(function($) {

    $(document).ready(function() {
        $('[data-toggle="tooltip"]').tooltip();
        $('[data-dj-messages-noty]').djMessagesNoty();
        $('[data-ajax-submit]').djangoAjaxForms();
    });

})(jQuery);
