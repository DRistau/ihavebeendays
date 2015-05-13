from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from ibeendays.tasks import views

router = routers.DefaultRouter()
router.register('tasks', views.TaskViewSet)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^tasks/', include('tasks.urls')),
    url(r'', include('core.urls')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
)
