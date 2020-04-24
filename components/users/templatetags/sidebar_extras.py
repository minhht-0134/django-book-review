from django.template.defaulttags import register
from components.users.models import User


@register.simple_tag
def get_total_member():
    return User.objects.count()
