from django.views.generic import ListView, detail
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from ..models import Book, Activity
from ..forms import BookListSearchForm

class BookListView(ListView):
  paginate_by = 8
  model = Book
  form_class = BookListSearchForm

  def get_queryset(self):
    filter_params = dict(self.request.GET)
    user_id = filter_params.get('user_id', [None])[0]
    if user_id is None or user_id == '': user_id = self.request.user.id
    activities = Activity.objects.filter(
        user_id=user_id,
        target_object_type_id=ContentType.objects.get(
          app_label='books', model='book').id
      )
    query_or = Q()

    if filter_params.get('reading', [None])[0] is not None:
      query_or |= Q(id__in=activities.filter(
        action_type=Activity.READ, status=Activity.READING).values('target_object_id'))

    if filter_params.get('readed', [None])[0] is not None:
      query_or |= Q(id__in=activities.filter(
        action_type=Activity.READ, status=Activity.READED).values('target_object_id'))

    if filter_params.get('favorite', [None])[0] is not None:
      query_or |= Q(id__in=activities.filter(
        action_type=Activity.FAVORITE).values('target_object_id'))

    if filter_params.get('pending', [None])[0] is not None:
      query_or |= Q(id__in=activities.filter(
        action_type=Activity.BUY, status=Activity.BUY_PENDING).values('target_object_id'))

    if filter_params.get('approve', [None])[0] is not None:
      query_or |= Q(id__in=activities.filter(
        action_type=Activity.BUY, status=Activity.BUY_APPROVE).values('target_object_id'))

    if filter_params.get('reject', [None])[0] is not None:
      query_or |= Q(id__in=activities.filter(
        action_type=Activity.BUY, status=Activity.BUY_REJECT).values('target_object_id'))

    query_and = Q()

    for field in ['title__contains', 'pub_date__lt', 'pub_date__gt']:
      field_filter = filter_params.get(field, [None])[0]
      if field_filter: query_and &= Q(**{field: field_filter})

    return Book.objects.filter(Q(query_or) & Q(query_and))

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context['form'] = self.form_class(self.request.GET)

    return context

class BookDetailView(detail.DetailView):
  model = Book

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    user = self.request.user
    book = kwargs['object']

    context['read'] = book.activities().filter(
      user_id=user.id, action_type=Activity.READ).first()
    context['favorite'] = book.activities().filter(
      user_id=user.id, action_type=Activity.FAVORITE).first()
    context['buy'] = book.activities().filter(
      user_id=user.id, action_type=Activity.BUY).first()
    context['rate'] = book.activities().filter(
      user_id=user.id, action_type=Activity.RATE).first()

    return context
