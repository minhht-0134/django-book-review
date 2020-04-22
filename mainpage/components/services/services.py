from books.models import *

def check_logged(request):
    if request.user.is_authenticated:
        current_user = request.user
        return True, current_user
    return False, None

def check_favorite(model, book, user):
    try:
        model.objects.get(user=user, book=book)
        return True
    except:
        return False

def check_mark(model, book, user):
    read = False
    reading = False
    try:
        mark = model.objects.get(user=user, book=book)
        if mark.type == 'read':
            read = True
        elif mark.type == 'reading':
            reading = True
        return read, reading
    except:
        return read, reading

def check_rate(user, book):
    try:
        check_rate = Rate.objects.get(user=user, book=book)
        return check_rate
    except:
        return False
    
def check_request(user, book):
    try:
        req = RequestBook.objects.get(user=user, book=book)
    except:
        return None
    return req.status
    