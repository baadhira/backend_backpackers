
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve 
from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/',include('app.urls')),
    path('eventapi/',include('event.urls')),
    path('discussionapi/',include('discussion.urls')),
    path('chat/',include('chat.urls')),
    path('message/',include('messagecontrol.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

    # path('', include('rest_friendship.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

