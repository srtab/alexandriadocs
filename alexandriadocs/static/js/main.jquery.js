/* globals jQuery */
"use strict";

(function($) {

  $(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-dj-messages-noty]').djMessagesNoty();
    $('[data-ajax-submit]').djangoAjaxForms();

    $('.select2').each(function() {
      var $this = $(this),
          options = {};

      if ($this.data('autocomplete-url')) {
        options.ajax = {
          url: $this.data('autocomplete-url'),
          delay: 250,
          cache: true,
          data: function (params) {
            var query = {
              term: params.term,
              page: params.page || 1
            }
            return query;
          },
        }
      }

      $(this).select2(options);
    });
  });

})(jQuery);
