$('#review_button').on('click', function(e) {
  e.preventDefault()

  var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val()
  var content = $('input[name="review"]').val()
  var target_object_id = $('#book_detail').attr('data-book-id')
  var username = $('#book_detail').attr('data-username')

  $.ajax({
    url: '/activities/',
    type: 'POST',
    data: {
      csrfmiddlewaretoken,
      target_object_type: 'book',
      target_object_id,
      action_type: 1,
      content,
    },
    success: function(data) {
      var review = $('.book_review:first').clone()

      review.find('h6:first').html(username)
      review.find('.book_review_content').html('"' + content + '"')
      review.removeClass('d-none')
      review.attr('data-id', data.id)

      $('.book_review_list').prepend(review)
    }
  })
})

$('.book_review_list').on('click', '.reply', function() {
  var exiting_comment_form =
    $(this).closest('.book_review').find('.book_review_comment_form')

  if (exiting_comment_form.length > 0) return exiting_comment_form.remove()

  var comment_form = $('.book_review_comment_form:first').clone()

  comment_form.attr('data-type', 'reply')
  comment_form.removeClass('d-none')

  $(this).closest('.book_review')
    .find('.book_review_comment_list').prepend(comment_form)
})

$('.book_review_list').on('click', '.edit', function() {
  var exiting_comment_form =
    $(this).closest('.book_review').find('.book_review_comment_form')

  if (exiting_comment_form.length > 0) return exiting_comment_form.remove()

  var comment_form = $('.book_review_comment_form:first').clone()
  var old_content = $(this).closest('.book_review_detail')
    .find('.book_review_content').html()

  comment_form.find('input[name="comment"]').val(old_content.slice(1,-1))
  comment_form.attr('data-type', 'edit')
  comment_form.removeClass('d-none')

  $(this).closest('.book_review')
    .find('.book_review_comment_list').prepend(comment_form)
})

$('.book_review_list').on('click', '.submit_comment', function() {
  var comment_form = $(this).closest('.book_review_comment_form')
  var content = comment_form.find('input[name="comment"]').val()
  var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val()
  var target_object_id = comment_form.closest('.book_review').attr('data-id')
  var username = $('#book_detail').attr('data-username')
  var $book_review_comment_list = $(this).closest('.book_review_comment_list')

  if (comment_form.attr('data-type') === 'reply') {
    $.ajax({
      url: '/activities/',
      type: 'POST',
      data: {
        csrfmiddlewaretoken,
        target_object_type: 'activity',
        target_object_id,
        action_type: 1,
        content,
      },
      success: function(data) {
        comment_form.remove()

        var comment = $('.book_review_comment:first').clone()

        comment.find('h6:first').html(username)
        comment.find('.book_review_comment_content').html('"' + content + '"')
        comment.removeClass('d-none')
        comment.attr('data-id', data.id)

        $book_review_comment_list.prepend(comment)
      }
    })
  } else {
    $.ajax({
      url: '/activities/' + target_object_id + '/change/',
      type: 'POST',
      data: {
        csrfmiddlewaretoken,
        content: content,
      },
      success: function(data) {
        comment_form.closest('.book_review')
          .find('.book_review_content').html('"' + data.content + '"')
        comment_form.remove()
      }
    })
  }
})

$('.book_review_list').on('click', '.delele', function() {
  var book_review = $(this).closest('.book_review')
  var activity_id = book_review.attr('data-id')
  var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val()

  $.ajax({
    url: '/activities/' + activity_id + '/delete/',
    type: 'POST',
    data: {
      csrfmiddlewaretoken
    },
    success: function() {
      book_review.remove()
    }
  })
})
