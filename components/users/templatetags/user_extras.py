from django.template.defaulttags import register


@register.filter
def get_item_dictionary(dictionary, key):
    return dictionary.get(key)



