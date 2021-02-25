from django import template
from django.template.defaultfilters import stringfilter

from catalog.models import Book_read

register = template.Library()


@register.filter(name='check_books')
@stringfilter
def check_books(book_instance_id, user_instance_id):
    if Book_read.objects.filter(book_id=book_instance_id, user_id=user_instance_id, active=1).exists() is False:
        return False
    else:
        return True