from books.models import *
from mainpage.components.services import services

def get_one_or_all_or_count(model, pk=None):
    item = None
    if pk:
        item = model.objects.get(pk=pk)
    items = model.objects.all()
    count = items.count()
    return item, items, count

def save_action(user, content, type_action):
    action = Action(
        user=user,
        type_action=type_action,
        content_action=content
    )
    action.save()
    
def have_rate(book, check_rate, rate_data, review_data):
    old_rate = check_rate.score
    book.score_rate = book.score_rate - old_rate + int(rate_data)
    book.save()
    
    check_rate.score = rate_data
    check_rate.review = review_data
    check_rate.edited = True
    check_rate.save()

    content = f"You have edited the '{book.title}' book review"
    save_action(user, content, 'edited')
    
def havent_rate(book, user, rate_data, review_data):
    create_rate = Rate(
        book=book,
        user=user,
        score=rate_data,
        review=review_data,
    )
    create_rate.save()
    
    old_score = book.score_rate
    old_total = book.total_rate
    book.score_rate = old_score + int(rate_data)
    book.total_rate = old_total + 1
    book.save()

    content = f"You have rated the '{book.title}' book review"
    save_action(user, content, 'rated')

def my_favorites(current_user):
    item = Favorite.objects.filter(user=current_user)
    return item

def my_mark(current_user):
    read = MarkBook.objects.filter(user=current_user, type='read')
    reading = MarkBook.objects.filter(user=current_user, type='reading')
    return read, reading

def my_actions(current_user):
    items = Action.objects.filter(user=current_user).order_by('-time_action')[:100]
    return items

def mark_read_or_reading(pk, current_user, type_mark):
    book = Book.objects.get(pk=pk)
    try:
        mark = MarkBook.objects.get(
            book=book,
            user=current_user
        )
        mark.type = type_mark
        mark.save()
    except:
        mark = MarkBook(
            user=current_user,
            book=book,
            type=type_mark
        )
        mark.save()
    content = f"You have marked the '{book.title}' book as {type_mark}"
    save_action(current_user, content, 'add')
    
def add_favorite(user, book):
    try:
        Favorite.objects.get(
            user=user,
            book=book
        )
    except:
        favorite = Favorite(
            user=user,
            book=book
        )
        favorite.save()
        
        content = f"You have added the '{book.title}' to your favorites"
        save_action(user, content, 'added')
        
def remove_favorite(user, book):
    favorited = Favorite.objects.get(
        user=user,
        book=book
    )
    favorited.delete()
    content = f"You have removed the '{book.title}' from your favorites"
    save_action(user, content, 'removed')

def create_comment(rate_id, content, user):
    rate = Rate.objects.get(pk=rate_id)
    comment = Comment(
        user=user,
        rate=rate,
        content=content
    )
    comment.save()
    content = f"You commented to the review of '{rate.user}'"
    save_action(user, content, 'responded')
    
def delete_comment(comment_id, user):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    content = f"You have deleted your comment"
    save_action(user, content, 'deleted')
    
def edit_comment(comment_id, user, content_data):
    comment = Comment.objects.get(pk=comment_id)
    comment.content = content_data
    comment.save()
    content = f"You have edited your comment"
    save_action(user, content, 'edited')

def send_request_book(user, pk):
    book = Book.objects.get(pk=pk)
    try:
        requestbook = RequestBook.objects.get(
            user=user,
            book=book
        )
        requestbook.status = 'pending'
        requestbook.save()
    except:
        request_book = RequestBook(
            user=user,
            book=book
        )
        request_book.save()
    content = f"You have sent a request to buy a new '{book.title}' book."
    save_action(user,content, 'add')
        
def cancel_request(user, pk):
    try:
        book = Book.objects.get(pk=pk)
        find_request = RequestBook.objects.get(
            user=user,
            book=book,
        )
        find_request.status = 'canceled'
        find_request.save()
        content = f"You have canceled a request to buy a new '{book.title}' book."
        save_action(user,content, 'add')
    except:
        pass

def list_request(current_user):
    items = RequestBook.objects.filter(user=current_user).order_by('-status')
    return items
