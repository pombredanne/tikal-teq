from django.conf.urls import patterns, include, url
from django.conf.urls import patterns, url, include
from rest_framework import routers
from rest import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# Uncomment the next two lines to enable the admin:

admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^teq/', include('core.urls')),
    url(r'^api/', include('rest.urls')),
) #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
