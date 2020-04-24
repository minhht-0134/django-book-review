jQuery(document).ready(function () {

    let url = $('.fashion-tag-select2').attr('data-url');

    $.ajax({
        url: url,
        method: 'GET',
        statusCode: {
            404: function () {
                grow('error get tags', 'danger');
            },
            200: function (tags) {
                $("#select2_sample5").select2({
                    tags: tags
                });
            }
        }
    });
});