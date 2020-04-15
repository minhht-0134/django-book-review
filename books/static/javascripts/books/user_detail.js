$('.follow_button').on('click', function() {
  var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val()
  var $this = $(this)
  var target_object_id = $this.attr('data-target-id')
  var activity_id = $this.attr('data-activity-id')
  var url = /activities/
  if (activity_id) url = url + activity_id + '/delete/'

  $.ajax({
    url,
    type: 'POST',
    data: {
      csrfmiddlewaretoken,
      target_object_type: 'user',
      target_object_id,
      action_type: 4,
    },
    success: function(data) {
      window.location.reload()

      if (data.id) {
        $this.attr('data-activity-id', data.id)
        $this.html('UnFollow')
      } else {
        $this.attr('data-target-id', target_object_id)
        $this.attr('data-activity-id', '')
        $this.html('Follow')
      }
    }
  })
})
