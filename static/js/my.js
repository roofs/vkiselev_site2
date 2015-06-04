function scrollNav() {
    $('a.slide').click(function (e) {
        if (window.location.pathname == "/") {
            var href = $(this).attr('href');
            var idx = href.indexOf("#")
            var anchor = idx != -1 ? href.substring(idx) : "";
            if (anchor && $(anchor)) {
                e.preventDefault();
                var scrollTop;
                if (anchor == "#")
                    scrollTop = 0;
                else
                    scrollTop = $(anchor).offset().top-20;
                $('html, body').stop().animate({
                    scrollTop: scrollTop
                }, 400);
                window.history.replaceState(null, null, anchor);
            }
        }
    });
}

window.setup_ajax = function (csrftoken) {
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
};