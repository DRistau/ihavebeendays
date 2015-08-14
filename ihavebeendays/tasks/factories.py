import factory
from ihavebeendays.core.factories import UserFactory
from ihavebeendays.tasks.models import Task


class TaskFactory(factory.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'Task {0}'.format(n))
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Task
        django_get_or_create = ('title', )
