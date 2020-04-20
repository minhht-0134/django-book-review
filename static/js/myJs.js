(function ($) {
  "use strict";
    $('#inner_search').keyup(function () {
        const value_search = this.value
        const temp = `<a href=\"?category=all&page=1&search=${value_search}"><i class=\"ti-search\"></i></a>`
        $('#inputGroupPrepend').html(temp)
    })

    $('.ratebook').click(function() {
        const getAttr = $(this).attr('for')
        const value = $("#"+getAttr).val()
        $('#selectedRate').val(value)
    });
}(jQuery));