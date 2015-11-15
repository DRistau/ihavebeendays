import pytest
from django.utils import timezone
from .core.factories import UserFactory
from .tasks.factories import TaskFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def user(db):
    return UserFactory.create()


@pytest.fixture
def task(db):
    now = timezone.now()
    three_days_behind = now - timezone.timedelta(days=3)

    return TaskFactory.create(
        uuid='7F1741B8-6CBD-4DE7-B324-8840D643E08A',
        title='Factored Task',
        started_at=three_days_behind,
        finished_at=now,
    )


@pytest.fixture
def unfinished_tasks(db, user):
    started_at = timezone.now() - timezone.timedelta(days=1)
    return TaskFactory.create_batch(1, uuid='7F1741B8-6CBD-4DE7-B324-8840D643E08A', title='Unfinished Task', user=user,
                                    started_at=started_at)


@pytest.fixture
def finished_tasks(db, user):
    started_at = timezone.datetime(2015, 2, 9, 12, 0, 0)
    finished_at = timezone.datetime(2015, 2, 10, 12, 0, 0)
    last_longer_duration = 1
    return TaskFactory.create_batch(3, user=user, started_at=started_at,
                                    finished_at=finished_at,
                                    last_longer_duration=last_longer_duration)


@pytest.fixture
def logged_in_request(client, user):
    client.login(username='test', password='test')

    def lazy(url):
        return client.get(url)

    return lazy
