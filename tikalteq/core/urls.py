from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
#admin.autodiscover()
from views import teq_form,teq_report,candidates

urlpatterns = patterns('',
    url(r'^teq_form/(?P<uuid>\w+)/$',  teq_form, name="teq_form"),
    url(r'^teq_report/(?P<uuid>\w+)/$',  teq_report, name="teq_report"),
    url(r'^candidates/$',  candidates, name="candidates")
)
