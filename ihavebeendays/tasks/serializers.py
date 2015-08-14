from ihavebeendays.tasks.models import Task
from rest_framework import serializers


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Task
        fields = ('title', 'user', 'started_at', 'finished_at', )
