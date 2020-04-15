from django.views.generic import ListView, detail

from ..models import Book, Activity

class BookListView(ListView):
  model = Book
  queryset = Book.objects.all()

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
