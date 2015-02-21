from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hannibal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^get_thumbs/(?P<channel_id>\d+)/', 'thumbs.views.get_thumbs',
        name='get_thumbs'),
)
