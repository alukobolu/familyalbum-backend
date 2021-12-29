from django.urls import path, include
from . import views

app_name = "albums_api"

urlpatterns = [
    path('upload', views.file_upload.as_view(), name='upload'),# done

    path('view/<str:fileid>', views.view_one_file.as_view(), name='view_one_file'),

    path('view_all_files/<albumid>', views.view_all_files.as_view(), name='view_all'),# done
    path('favourites/', views.view_all_favourites.as_view(), name='view_all_favourites'), # not now
    path('deleted/', views.view_all_deleted.as_view(), name='view_all_deleted'),
    
    path('view/favourite/', views.favourite_file.as_view(), name='favourite'),#not now
    path('view/delete/', views.delete_file.as_view(), name='delete'),# not now

    path('rename/<id>', views.rename.as_view(), name='rename'),# not now
    path('change_privacy/', views.change_privacy.as_view(), name='change_privacy'), #not now

    path('album/create/', views.create_album.as_view(), name='create_album'),# done
    path('album', views.view_all_albums.as_view(), name='view_all_albums'),# done
    
    path('edit_member/', views.edit_members.as_view(), name='edit_members'),
    path('view_members/<str:album_id>', views.view_all_members.as_view(), name='view_members'),

    path('permanent_delete', views.permanent_delete.as_view(), name='permanent_delete'),#not now

    path('feeds/', include('feeds.urls')),

]