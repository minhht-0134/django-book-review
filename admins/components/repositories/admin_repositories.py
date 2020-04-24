from books.models import *
from django.db.models import Count

def save_action(user, content, type_action):
    action = Action(
        user=user,
        type_action=type_action,
        content_action=content
    )
    action.save()

def count_model(model, condition = None):
    count = model.objects.all().count()
    if condition == 'user':
        count = model.objects.filter(is_superuser=0).count()
    return count

def top_favorite():
    items = []
    favorite = Favorite.objects.values('book').annotate(dcount=Count('book')).order_by('-dcount', 'book')[:4]
    for item in favorite:
        book = Book.objects.get(pk=item.get('book'))
        items.append([book, item.get('dcount')])
    return items

def top_rate ():
    items = []
    books = Book.objects.all()
    for book in books:
        items.append([book, float(book.get_star())])
    items.sort(key=lambda x: x[1], reverse=True)
    return items[:4]

def top_mark(typemark):
    items = []
    markread = MarkBook.objects.filter(type=typemark).values('book').annotate(dcount=Count('type')).order_by('-dcount', 'book')[:4]
    for item in markread:
        book = Book.objects.get(pk=item.get('book'))
        items.append([book, item.get('dcount')])
    return items

def change_status_request(request_id, status, request):
    request_item = RequestBook.objects.get(pk=request_id)
    request_item.status = status
    request_item.save()

    content = f"You have {status} request of '{request_item.user}'"
    save_action(request.user, content, 'added')
    