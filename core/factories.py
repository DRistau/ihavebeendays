import factory
from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    username = 'test'
    email = 'test@test.com'
    password = factory.PostGenerationMethodCall('set_password', 'test')
    is_active = True

    class Meta:
        model = User
