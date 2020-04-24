(function ($) {
    "use strict";

    $('#choseCategory').val($('#selectCategory :selected').val())
    $('#selectCategory').change(function () {
        let valueSelect = this.options[this.selectedIndex].value
        $('#choseCategory').val(valueSelect)
    })

    $('.confirm_delete').click(function () {
        return confirm('Are you sure you want to delete this?');
    })
}(jQuery));