from django.urls import path, include
from . import views

app_name = "documents_api"

urlpatterns = [
    path('home/', views.document_upload, name='upload'),
    path('upload', views.document_upload.as_view(), name='upload'),
    path('view/', views.document_allview.as_view(), name='view_all'),
    path('favourites/', views.document_allview_favourites.as_view(), name='view_all_favourites'),
    path('deleted/', views.document_allview_deleted.as_view(), name='view_all_deleted'),
    path('view/<str:documentid>', views.document_singleview.as_view(), name='view_single'),
    path('view/favourite/', views.document_fav.as_view(), name='favourite'),
    path('view/delete/', views.document_delete.as_view(), name='delete'),
]