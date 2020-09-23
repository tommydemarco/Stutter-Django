from django.urls import path

from .views import *

urlpatterns = [
    path('', post_list_view),
    path('action/', post_action_view),
    path('create/', post_create_view),
    path('<int:post_id>/', post_detail_view),
    path('<int:post_id>/delete/', post_delete_view),
]