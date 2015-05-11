import hashlib
from django import template

GRAVATAR_URL = "https://www.gravatar.com/avatar/{hash}?s=48&d=mm"

register = template.Library()


@register.simple_tag
def gravatar_from_email(email=None):
    m = hashlib.md5()
    m.update(email.encode('utf-8'))
    md5_hash = m.hexdigest()

    return GRAVATAR_URL.format(hash=md5_hash)
