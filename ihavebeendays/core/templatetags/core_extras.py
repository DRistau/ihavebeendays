import hashlib
from django import template
from django.utils import timezone

GRAVATAR_URL = "https://www.gravatar.com/avatar/{hash}?s=48&d=mm"
DATE_OF_THE_FIRST_PROJECT_COMMIT = timezone.datetime(2015, 1, 23, 19, 7, 0,
                                                     tzinfo=timezone.get_current_timezone())

register = template.Library()


@register.simple_tag
def example_days_duration(since=DATE_OF_THE_FIRST_PROJECT_COMMIT):
    delta = (timezone.now() - since)
    return delta.days


@register.simple_tag
def gravatar_from_email(email=None):
    m = hashlib.md5()
    m.update(email.encode('utf-8'))
    md5_hash = m.hexdigest()

    return GRAVATAR_URL.format(hash=md5_hash)
