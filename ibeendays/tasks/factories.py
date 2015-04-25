import factory
from ibeendays.core.factories import UserFactory
from ibeendays.tasks.models import Task


class TaskFactory(factory.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'Task {0}'.format(n))
    user = UserFactory.create()

    class Meta:
        model = Task
