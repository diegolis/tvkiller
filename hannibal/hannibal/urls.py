from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hannibal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^get_thumbs/(?P<channel_id>\d+)/', 'thumbs.views.get_thumbs',
        name='get_thumbs'),
    url(r'^get_thumb/(?P<thumb_id>\d+)/', 'thumbs.views.get_thumb',
        name='get_thumb'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
