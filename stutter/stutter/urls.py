from django.conf import settings 
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, re_path, include # url()
from django.views.generic import TemplateView

from posts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('add-post/', post_create_view),
    path('posts/', post_list_view),
    path('posts/<int:post_id>/', post_detail_view),
    path('api/posts/', include('posts.urls')),
    #testing react
    path('react', TemplateView.as_view(template_name="react.html"))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
