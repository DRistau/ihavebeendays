from django.utils import timezone
from ibeendays.core.templatetags import core_extras


def test_gravatar_from_email():
    gravatar = core_extras.gravatar_from_email(email='gandalf@middleearth.com')

    assert gravatar == 'https://www.gravatar.com/avatar/a8923217408354fc73bfd3e33efd4331?s=48&d=mm'


def test_example_days_duration():
    yesterday = timezone.now() - timezone.timedelta(days=1)
    days = core_extras.example_days_duration(yesterday)

    assert days == 1
