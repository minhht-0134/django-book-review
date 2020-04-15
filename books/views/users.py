from django.views.generic import detail
from django.contrib.contenttypes.models import ContentType

from ..models import User, Book, Activity

class UserDetailView(detail.DetailView):
  model = User
  template_name = 'books/user_detail.html'

  def get_context_data(self, **kwargs):
    MAX_EXTRA_RECORD = 3

    context = super().get_context_data(**kwargs)

    current_user = self.request.user
    user = kwargs['object']

    activities = Activity.objects.filter(user_id=user.id)

    context['follow_act'] = Activity.objects.filter(
      user_id=current_user.id,
      target_object_id=user.id,
      target_object_type_id=ContentType.objects.get(
        app_label='auth', model='user').id,
      action_type=Activity.FOLLOW).first()

    following = Activity.objects.filter(
      target_object_id=user.id,
      target_object_type_id=ContentType.objects.get(
        app_label='auth', model='user').id,
      action_type=Activity.FOLLOW)
    context['following_count'] = following.count()
    context['following_users'] = User.objects.filter(
      id__in=[a.user_id for a in following[:MAX_EXTRA_RECORD]])

    followed = Activity.objects.filter(
      user_id=user.id,
      target_object_type_id=ContentType.objects.get(
        app_label='auth', model='user').id,
      action_type=Activity.FOLLOW)
    context['followed_count'] = followed.count()
    context['followed_users'] = User.objects.filter(
      id__in=[a.target_object_id for a in followed[:MAX_EXTRA_RECORD]])

    reading = activities.filter(
      target_object_type_id=ContentType.objects.get(
        app_label='books', model='book').id,
      action_type=Activity.READ,
      status=Activity.READING)

    context['reading_count'] = reading.count()
    context['reading_books'] = Book.objects.filter(
      id__in=[a.target_object_id for a in reading[:MAX_EXTRA_RECORD]])

    readed = activities.filter(
      target_object_type_id=ContentType.objects.get(
        app_label='books', model='book').id,
      action_type=Activity.READ,
      status=Activity.READED)

    context['readed_count'] = readed.count()
    context['readed_books'] = Book.objects.filter(
      id__in=[a.target_object_id for a in readed[:MAX_EXTRA_RECORD]])

    favorite = activities.filter(
      target_object_type_id=ContentType.objects.get(
        app_label='books', model='book').id,
      action_type=Activity.FAVORITE)
    context['favorite_count'] = favorite.count()
    context['favorite_books'] = Book.objects.filter(
      id__in=[a.target_object_id for a in favorite[:MAX_EXTRA_RECORD]])

    review = activities.filter(
      target_object_type_id=ContentType.objects.get(
        app_label='books', model='book').id,
      action_type=Activity.COMMENT)

    context['review_count'] = review.count()
    context['reviews'] = review[:MAX_EXTRA_RECORD]

    context['activities'] = activities.filter(
      action_type__in=[Activity.COMMENT, Activity.READ, Activity.FAVORITE,
        Activity.FOLLOW, Activity.BUY]).exclude(
      target_object_type_id=ContentType.objects.get(
        app_label='books', model='activity').id)

    return context
