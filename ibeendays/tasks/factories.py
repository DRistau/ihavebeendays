import factory
from ibeendays.core.factories import UserFactory
from ibeendays.tasks.models import Task


class TaskFactory(factory.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'Task {0}'.format(n))
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Task
        django_get_or_create = ('title', )
