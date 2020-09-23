
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, re_path, include # url()

from posts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('add-post/', post_create_view),
    path('posts/', post_list_view),
    path('posts/<int:post_id>/', post_detail_view),
    path('api/posts/', include('posts.urls'))
]

