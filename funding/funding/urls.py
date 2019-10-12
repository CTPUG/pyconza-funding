from django.conf.urls import url, include
from rest_framework_extensions import routers

from .views import (
        ApplicationView, ApplicationCreate, ApplicationUpdate
    )

urlpatterns = [
    url(r'^new/$', ApplicationCreate.as_view(), name='funding_application_submit'),
    url(r'^(?P<pk>\d+)/$', ApplicationView.as_view(),
        name='funding_application'),
    url(r'^(?P<pk>\d+)/edit/$', ApplicationUpdate.as_view(),
        name='funding_application_edit'),
]
