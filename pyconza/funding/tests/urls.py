from django.conf.urls import url, include

urlpatterns = [
    url(r'^/', include('wafer.urls')),
    url(r'^funding/', include('pyconza.funding.urls')),
]
