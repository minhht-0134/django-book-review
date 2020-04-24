$(document).ready(function () {

    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });

    $(document).on('click', '.comment-reply', function () {
        let comment_id = $(this).attr('data-comment-id');
        let user_name = $(this).attr('data-user-name');

        let item = '.comment-show-' + comment_id;

        $(item + ' .comment-body').val('@' + user_name + ' ');

        $(item + ' .comment-input').show();
    });

    $(document).on('click', '.fashion-comment-store', function () {
        let body;

        let comment_body = $(this).parent('.fashion-comment-relative')
            .children('.form-group')
            .children('.comment-body');

        if (body = comment_body.val().trim()) {
            let data_html = $('.data-comment-ajax');
            let data_commentable = $('.data-commentable');

            let url = data_html.attr('data-url');
            let parent_id = $(this).attr('data-parent-id');
            let commentable_id = data_commentable.attr('data-commentable-id');
            let commentable_type = data_commentable.attr('data-commentable-type');
            let avatar = data_html.attr('data-avatar');
            let user_id = data_html.attr('data-user-id');


            let data = {
                commentable_id: commentable_id,
                commentable_type: commentable_type,
                user_id: user_id,
                parent_id: parent_id,
                body: body
            };

            $.ajax({
                url: url,
                method: 'POST',
                data: data,
                dataType: 'json',
                statusCode: {
                    404: function () {
                        alert('error');
                    },
                    200: function (data) {
                        if (parent_id) {
                            $('.comment-div-' + parent_id).append("<div class='media comment-delete-" + data.comment_id + "'><a href='javascript:void(0);' class='pull-left'><img src='" + avatar + "' alt='' class='media-object'> </a> <div class='media-body'><h4 class='media-heading'>" + data.user_name + "<span>" + data.time + " | <a class='comment-reply' data-comment-id='" + parent_id + "' data-user-name='" + data.user_name + "'>" + data.label.reply + "</a> | <a class='comment-delete-item' data-url='" + data.url_destroy + "' data-comment-delete-id='" + data.comment_id + "'>" + data.label.delete + "</a></span></h4><p>" + body + "</p></div></div>");
                        } else {
                            $('.comment-div').append("<div class='media comment-delete-" + data.comment_id + "'><a href='javascript:void(0);' class='pull-left'><img src='" + avatar + "' alt='' class='media-object'> </a> <div class='media-body comment-show-" + data.comment_id + "'><h4 class='media-heading'>" + data.user_name + "<span>" + data.time + " | <a class='comment-reply' data-comment-id='" + data.comment_id + "' data-user-name='" + data.user_name + "'>" + data.label.reply + "</a> | <a class='comment-delete-item' data-url='" + data.url_destroy + "' data-comment-delete-id='" + data.comment_id + "'>" + data.label.delete + "</a></span></h4><p>" + body + "</p><div class='comment-div-" + data.comment_id + "'></div><div class='comment-input fashion-comment-relative fix-relative'><div class='form-group fashion-comment-input'><input type='text' class='form-control comment-body'></div><span class='btn btn-primary fashion-comment-store fix-comment' data-parent-id='" + data.comment_id + "'>" + data.label.send + "</span></div></div></div>");
                        }

                        comment_body.val('');
                    }
                }
            });
        } else {
            return false;
        }
    });

    $(document).on('click', '.comment-delete-item', function () {
        let id = $(this).attr('data-comment-delete-id');
        let url = $(this).attr('data-url');

        let data = {
            _method: 'delete'
        };

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
                    $('.comment-delete-' + id).remove();
                }
            }
        });
    });

    $('.fashion-review-store').click(function () {
        let url = $(this).attr('data-url');
        let product_id = $(this).attr('data-product-id');
        let content = $('.fashion-review-content').val().trim();
        let rating = $('.fashion-review-rating').val();

        let data = {
            product_id: product_id,
            content: content,
            rating: rating
        };

        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            dataType: 'json',
            statusCode: {
                404: function () {
                    alert('error');
                },
                200: function (data) {
                    $('.fashion-review-append').append("<div class='review-item clearfix'><div class='review-item-submitted'><strong>" + data.user_name + "</strong><em>" + data.time + "</em><div class='rateit' data-rateit-value='" + rating + "' data-rateit-ispreset='true' data-rateit-readonly='true'></div></div><div class='review-item-content'><p>" + content + "</p></div></div>");
                    $('.product-rating').html("<span class='rateit' data-rateit-value='" + data.product_rating + "' data-rateit-ispreset='true' data-rateit-readonly='true'></span>");
                    $('.fashion-review-content').val('');
                    $('div.rateit, span.rateit').rateit();
                }
            }
        });

        return false;
    });

    $('.fashion-wish-list-destroy').click(function () {
        let title = $('.data-ajax-delete-product').attr('data-title');
        let message = $('.data-ajax-delete-product').attr('data-message');
        let url = $('.data-ajax-delete-product').attr('data-url');
        let product_id = $(this).attr('data-product-id');

        let data = {
            _method: 'delete',
            product_id: product_id
        };

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
                    $('.fashion-wish-list-' + product_id).remove();
                    showToast(title, message, 'success');
                }
            }
        });

        return false;
    });

    $('.add-to-wish-list').click(function () {
        let title = $(this).attr('data-title');
        let message = $(this).attr('data-message');
        let url = $(this).attr('data-url');
        let product_id = $(this).attr('data-product-id');

        let data = {
            product_id: product_id
        };

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
                    showToast(title, message, 'success');
                }
            }
        });

        return false;
    });

    $('.fashion-add-to-cart').click(function () {
        let title = $('.data-ajax').attr('data-title');
        let message = $('.data-ajax').attr('data-message');
        let url = $('.data-ajax').attr('data-url');
        let product_id = $(this).attr('data-product-id');
        let qty = $(this).parents('div').find('input').val();

        let data = {
            product_id: product_id,
            qty: qty
        };

        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            dataType: 'json',
            statusCode: {
                404: function () {
                    alert('error');
                },
                200: function (data) {
                    updateCart(data);
                    showToast(title, message, 'success');
                }
            }
        });

        return false;
    });

    $('.fashion-delete-item-cart').click(function () {
        let title = $('.data-ajax-delete-item-cart').attr('data-title');
        let message = $('.data-ajax-delete-item-cart').attr('data-message');
        let url = $('.data-ajax-delete-item-cart').attr('data-url');
        let cart_id = $(this).attr('data-cart-id');

        let data = {
            _method: 'delete',
            cart_id: cart_id
        };

        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            dataType: 'json',
            statusCode: {
                404: function () {
                    alert('error');
                },
                200: function (data) {
                    $('.cart-id-' + cart_id).remove();
                    $('.cart-total').text(currencyFormat(data.total));
                    updateCart(data);
                    showToast(title, message, 'success');
                }
            }
        });

        return false;
    });

    $('.change-qty-product-cart').change(function () {
        let title = $('.data-ajax-update-cart').attr('data-title');
        let message = $('.data-ajax-update-cart').attr('data-message');
        let url = $('.data-ajax-update-cart').attr('data-url');
        let cart_id = $(this).attr('data-cart-id');
        let qty = $(this).val();

        let data = {
            _method: 'patch',
            cart_id: cart_id,
            qty: qty
        };

        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            dataType: 'json',
            statusCode: {
                404: function () {
                    alert('error');
                },
                200: function (data) {
                    $('.cart-id-' + cart_id + ' .subtotal').text(currencyFormat(data.subtotal));
                    $('.cart-total').text(currencyFormat(data.total));
                    updateCart(data);
                    showToast(title, message, 'success');
                }
            }
        });

        return false;
    });

    function currencyFormat(value) {
        return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    function updateCart(data) {
        $('.fashion-cart-count').text(data.count);
        $('.fashion-cart-total').text(data.total);

        let html = '';

        for (let i = 0; i < data.content.length; i++) {
            html += "<li><a href='" + data.content[i].url + "'><img src='" + data.content[i].thumbnail + "' alt='" + data.content[i].name + "'></a><span class='cart-content-count'>x " + data.content[i].qty + "</span><strong><a href='" + data.content[i].url + "'>" + data.content[i].name + "</a></strong><em>" + data.content[i].price + "đ</em></li>";
        }

        $('.cart-pop').html(html);
    }

    function showToast(title, message, type) {
        toastr.options = {
            "closeButton": false,
            "debug": false,
            "positionClass": "toast-top-right",
            "onclick": null,
            "showDuration": "1000",
            "hideDuration": "1000",
            "timeOut": "1000",
            "extendedTimeOut": "1000",
            "showEasing": "swing",
            "hideEasing": "linear",
            "showMethod": "fadeIn",
            "hideMethod": "fadeOut"
        };

        toastr[type](message, title);
    }

});