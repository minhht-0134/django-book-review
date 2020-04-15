$('.book_info').on('click', '.book_info_action .read, .favorite, .buy',
  function() {
    var $this = $(this)
    var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val()
    var url = '/activities/';
    var activity_id = $this.find('h6').attr('data-id')
    var status = $this.find('h6').attr('data-status') || 0
    var action = $this.closest('div').attr('class').split()[0]
    var action_type = {read: 2, favorite: 3, buy: 5}[action]
    var target_object_id = $('#book_detail').attr('data-book-id')
    var target_object_type = 'book'

    if (activity_id) {
      url = url + activity_id + '/'
      if (action == 'favorite')
        url = url + 'delete/'
      else
        url = url + 'change/'
      if (action == 'read' && activity_id && status < 1) status++
    }

    $.ajax({
      url,
      type: 'POST',
      data: {
        csrfmiddlewaretoken,
        target_object_id,
        target_object_type,
        status,
        action_type
      },
      success: function(data) {
        var $h6 = $this.find('h6')
        $h6.attr('data-id', data.id || '')
        $h6.attr('data-status', data.status || '')

        if (!data.id) {
          $h6.removeClass('active').addClass('disactive')
        } else {
          $h6.removeClass('disactive').addClass('active')
          $h6.html(data.status_text)
        }
      }
    })
  })
