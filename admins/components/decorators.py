from django.shortcuts import redirect

def admin_required(function):
    def wrapper(request, *args, **kwargs):
        try:
            if not request.user.is_superuser:
                return redirect('mainpage')
            return function(request, *args, **kwargs)
        except:
            return redirect('mainpage')
    return wrapper
