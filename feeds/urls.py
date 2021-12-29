from django.urls import path, include
from . import views

app_name = "feeds_api"

urlpatterns = [
    path('post', views.posting.as_view(), name='posting'),
    path('comment', views.commenting.as_view(), name='commenting'),

    path('view_all/<albumid>', views.view_feed.as_view(), name='view_feed'),
    path('view_post/<postid>', views.view_post.as_view(), name='view_post'),
    path('view_comment/<postid>', views.view_comments.as_view(), name='view_comments'),

    path('delete_post', views.delete_post.as_view(), name='delete_post'),
    path('delete_comment', views.delete_comment.as_view(), name='delete_comment'),

]