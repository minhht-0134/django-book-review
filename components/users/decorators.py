from django.http import HttpResponseForbidden


def admin_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.role != 1:
            return HttpResponseForbidden('403 Forbidden')

        return function(request, *args, **kwargs)

    return wrapper
