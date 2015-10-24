from django.contrib import admin
from ihavebeendays.tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'title', 'user', )


admin.site.register(Task, TaskAdmin)
