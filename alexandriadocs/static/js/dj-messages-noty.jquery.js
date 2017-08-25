/* globals jQuery, Noty */

/******************************************************************
 * Integrate Noty with django messages.
 * Noty check for a ul element and create notification
 * to every li present and associate is class to notification type.
 * TODO: support alert and information type
 *
 * http://ned.im/noty/
 *****************************************************************/

"use strict";

(function($) {

    $.showMessages = function (type, content, options)
    {
        var icon_class = '';

        switch(type) {
            case 'success':
                icon_class = 'fa-check-circle';
                break;
            case 'warning':
                icon_class = 'fa-exclamation-triangle';
                break;
            case 'error':
                icon_class = 'fa-exclamation-circle';
                break;
            default:
                icon_class = 'fa-info-circle';
        }

        var icon = '<i class="fa fa-2x ' + icon_class + ' noty-icon" aria-hidden="true"></i>',
            text = "<div class='media'><span class='d-flex align-self-center'>" + icon + "</span><div class='media-body align-self-center'>" + content + "</div></div>";

        var settings = $.extend({
            text: text,
            type: type,
            theme: 'bootstrap-v4',
            timeout: 5000,
            progressBar: true,
        }, $.fn.djMessagesNoty.defaults, options);

        new Noty(settings).show();
    };

    $.fn.djMessagesNoty = function(options)
    {
        return this.each(function()
        {
            $(this).find('li').each(function() {
                var notification = $(this),
                    type = notification.attr('class');

                $.showMessages(type, notification.html(), options);
            });
        });
    };

    $.fn.djMessagesNoty.defaults = {};

})(jQuery);
