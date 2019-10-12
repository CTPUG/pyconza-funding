from django.conf.urls import url, include
from rest_framework_extensions import routers

from .views import (
        FundingApplicationView, FundingApplicationCreate, FundingApplicationUpdate
    )

urlpatterns = [
    url(r'^new/$', FundingApplicationCreate.as_view(), name='funding_application_submit'),
    url(r'^(?P<pk>\d+)/$', FundingApplicationView.as_view(),
        name='funding_application'),
    url(r'^(?P<pk>\d+)/edit/$', FundingApplicationUpdate.as_view(),
        name='funding_application_edit'),
]
