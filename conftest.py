import pytest
from django.utils import timezone
from core.factories import UserFactory
from tasks.factories import TaskFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def user(db):
    return UserFactory.create()


@pytest.fixture
def task(db):
    now = timezone.now()
    three_days_behind = now - timezone.timedelta(days=3)

    return TaskFactory.create(
        started_at=three_days_behind,
        finished_at=now,
    )


@pytest.fixture
def unfinished_tasks(db, user):
    return TaskFactory.create_batch(1, user=user)


@pytest.fixture
def finished_tasks(db, user):
    started_at = timezone.datetime(2015, 2, 9, 12, 0, 0)
    finished_at = timezone.datetime(2015, 2, 10, 12, 0, 0)
    return TaskFactory.create_batch(3, user=user, started_at=started_at,
                                    finished_at=finished_at)


@pytest.fixture
def logged_in_request(client, user):
    client.login(username='test', password='test')

    def lazy(url):
        return client.get(url)

    return lazy
