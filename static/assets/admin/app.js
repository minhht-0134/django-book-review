$(document).ready(function () {

    $.ajaxSetup({
        headers: {
            'X-CSRFToken': document.head.querySelector('meta[name="csrf-token"]').content,
        }
    });

    $('.fashion-delete-item').on('confirmed.bs.confirmation', function () {
        let id = $(this).attr('data-id');

        document.getElementById('delete-item-' + id).submit();
    });

    // Soft delete item
    $('.fashion-soft-delete-item').on('confirmed.bs.confirmation', function () {
        let url = $(this).attr('data-url');
        let message = $(this).attr('data-message');

        let item = $(this);

        $.ajax({
            url: url,
            method: 'POST',
            dataType: 'json',
            statusCode: {
                404: function () {
                    grow('error', 'danger');
                },
                403: function (error) {
                    grow(error.responseText, 'danger');
                },
                200: function () {
                    $('#sample_1').DataTable().row(item.parents('tr')).remove().draw();
                    item.parents('tr').remove();
                    grow(message, 'success');
                }
            }
        });
    });

    function grow(message, type) {
        $.bootstrapGrowl(message, {
            ele: 'body', // which element to append to
            type: type, // (null, 'info', 'danger', 'success', 'warning')
            offset: {
                from: 'top',
                amount: 100
            }, // 'top', or 'bottom'
            align: 'center', // ('left', 'right', or 'center')
            width: 'auto', // (integer, or 'auto')
            delay: 700, // Time while the message will be displayed. It's not equivalent to the *demo* timeOut!
            allow_dismiss: 0, // If true then will display a cross to close the popup.
            stackup_spacing: 0 // spacing between consecutively stacked growls.
        });
    }

    // Restore item
    $('.fashion-restore-item').click(function () {
        let url = $(this).attr('data-url');
        let message = $(this).attr('data-message');

        let data = {
            _method: 'put'
        };

        let item = $(this);

        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            dataType: 'json',
            statusCode: {
                404: function () {
                    alert('error');
                },
                200: function () {
                    $('#sample_2').DataTable().row(item.parents('tr')).remove().draw();
                    grow(message, 'success');
                }
            }
        });
    });

    // Force delete item
    $('.fashion-force-delete-item').on('confirmed.bs.confirmation', function () {
        let url = $(this).attr('data-url');
        let message = $(this).attr('data-message');

        let data = {
            _method: 'delete'
        };

        let item = $(this);

        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            dataType: 'json',
            statusCode: {
                404: function () {
                    grow('error', 'danger');
                },
                200: function () {
                    $('#sample_2').DataTable().row(item.parents('tr')).remove().draw();
                    grow(message, 'success');
                },
                201: function (data) {
                    alert(data);
                }
            }
        });
    });

    // Change status
    $('.fashion-change-status').change(function () {
        let url = $(this).attr('data-url');
        let status = parseInt($(this).val());
        let message = $(this).attr('data-message');
        let screen = $(this).data('screen');

        let item = $(this);

        item.attr('disabled', 'disabled');

        $.ajax({
            url: url,
            method: 'POST',
            data: {
                status
            },
            dataType: 'json',
            statusCode: {
                404: function (error) {
                    grow(error.responseText, 'danger');
                },
                403: function (error) {
                    grow(error.responseText, 'danger');

                    if (screen === 'request_index') {
                        item.val(3);
                        item.parents('tr')
                        .children('.pinky-book-action')
                        .children('span')
                        .addClass('disabled');
                        return;
                    }
                },
                200: function (result) {
                    grow(message, 'success');

                    if (screen === 'request_index' && status === 3) {
                        item.parents('tr')
                        .children('.pinky-book-action')
                        .children('span')
                        .addClass('disabled');
                        return;
                    }

                    item.removeAttr('disabled');
                }
            }
        });
    });

    // Change brand_id
    $('.fashion-change-brand').change(function () {
        $('.fashion-change-brand').attr('disabled', 'disabled');
        let message = $(this).attr('data-message');

        let url = $(this).attr('data-url');
        let brand_id = $(this).val();
        let user_id = $('.fashion-ajax').attr('data-user-id');

        let data = {
            user_id: user_id,
            brand_id: brand_id,
            _method: 'put'
        };

        let item = $(this);

        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            dataType: 'json',
            statusCode: {
                404: function () {
                    grow('error', 'danger');
                },
                200: function (result) {
                    $('.fashion-change-brand').removeAttr('disabled');

                    grow(message, 'success');

                    item.parents('tr')
                    .children('.fashion-time')
                    .css('color', 'green')
                    .css('font-weight', 'bold')
                    .html(result.time);

                    item.parents('tr')
                    .children('.fashion-user')
                    .css('color', 'green')
                    .css('font-weight', 'bold')
                    .html(result.user_name);
                }
            }
        });
    });

    // Change favorite
    $('.fashion-toggle').click(function () {
        let message_create = $(this).data('message-create');
        let message_delete = $(this).data('message-delete');
        let screen = $(this).data('screen');
        let icon_class_create = $(this).data('icon-class-create');
        let icon_class_delete = $(this).data('icon-class-delete');
        let url = $(this).attr('data-url');

        let item = $(this);

        $.ajax({
            url: url,
            method: 'POST',
            dataType: 'json',
            statusCode: {
                404: function () {
                    grow('error', 'danger');
                },
                200: function (result) {
                    let message = '';

                    if (result.responseText === 'create') {
                        item.removeClass(icon_class_delete)
                        .addClass(icon_class_create);

                        if (screen === 'member_index') {
                            item.html("&nbsp;Đang theo dõi")
                        }

                        message = message_create;
                    }
                    if (result.responseText === 'delete') {
                        item.removeClass(icon_class_create)
                        .addClass(icon_class_delete);

                        if (screen === 'member_index') {
                            item.html("&nbsp;Theo dõi")
                        }

                        message = message_delete;
                    }

                    grow(message, 'success');
                }
            }
        });
    });

    $('.read-notification').click(function () {
        let url = $(this).attr('data-url');
        let data = {
            '_method': 'patch'
        };

        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            dataType: 'json',
            statusCode: {
                404: function () {
                    grow('error', 'danger');
                }
            }
        });
    });

    // Upload file
    $('.fashion-upload-file').change(function (e) {
        let file = e.target.files || e.dataTransfer.files;
        let reader = new FileReader();

        reader.onload = (e) => {
            $('.fashion-image-upload img').attr('src', e.target.result);
        };

        reader.readAsDataURL(file[0]);
    });

    let sort_order;

    let updateOutput = function (e) {
        let list = e.length ? e : $(e.target);

        if (window.JSON) {
            sort_order = list.nestable('serialize');
        } else {
            grow('JSON browser support required for this demo.', 'danger');
        }
    };

    let nestable_list_1 = $('#nestable_list_1');
    let maxDepth = parseInt($('.fashion-nestable').attr('data-max-depth'));

    nestable_list_1.nestable({group: 1, maxDepth: maxDepth}).change(updateOutput);

    updateOutput(nestable_list_1);

    $('.fashion-save-sort-order').click(function () {
        let url = $(this).attr('data-url');
        let message = $(this).attr('data-message');

        let data = {
            _method: 'put',
            sort_order: sort_order
        };

        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            dataType: 'json',
            statusCode: {
                404: function () {
                    grow('error', 'danger');
                },
                200: function () {
                    grow(message, 'success');
                }
            }
        });
    });

    $('#book-detail-comment-create').click(function () {
        let url = $(this).data('url');
        let content = $('#book-detail-comment-content').val();
        let username = $(this).data('username');
        let avatar = $(this).data('avatar');

        $.ajax({
            url: url,
            method: 'POST',
            data: {
                content
            },
            dataType: 'json',
            statusCode: {
                404: function () {
                    grow('error', 'danger');
                },
                200: function () {
                    $('#book-detail-comment-content').val('');
                    $('#book-detail-comment-main').append(`
                        <div class="media">
                          <span class="pull-left">
                            <img alt="" src="${avatar}" class="media-object">
                          </span>
                          <div class="media-body">
                            <h4 class="media-heading">
                              ${username}
                            </h4>
                            <p>${content}</p>
                          </div>
                        </div>
                    `);
                }
            }
        });
    });

    $('#book-detail-review-create').click(function () {
        let url = $(this).data('url');
        let content = $('#book-detail-review-content').val();
        let rating = $('.book-detail-review-rating').val();
        let username = $(this).data('username');
        let avatar = $(this).data('avatar');

        $.ajax({
            url: url,
            method: 'POST',
            data: {
                content,
                rating
            },
            dataType: 'json',
            statusCode: {
                404: function () {
                    grow('error', 'danger');
                },
                200: function () {
                    $('#book-detail-review-content').val('');
                    $('#book-detail-review-main').append(`
                        <div class="media">
                          <span class="pull-left">
                            <img alt="" src="${avatar}" class="media-object">
                          </span>
                          <div class="media-body">
                            <h4 class="media-heading">
                              ${username}
                              <span>
                                <div
                                    class="rateit"
                                    data-rateit-value="${rating}"
                                    data-rateit-ispreset="true"
                                    data-rateit-readonly="true"
                                  >
                                  </div>
                              </span>
                            </h4>
                            <p>${content}</p>
                          </div>
                        </div>
                    `);
                    $('div.rateit, span.rateit').rateit();
                }
            }
        });
    });

});