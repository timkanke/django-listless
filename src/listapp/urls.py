from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views
# from .models import Item

app_name = 'listapp'
# example_urlpatterns = [
#     path('', views.ExampleUpdateView.as_view(), name='_list'),
#     path('new/', views.ExampleUpdateView.as_view(), name='_create'),
#     path('<int:pk>/', views.ExampleUpdateView.as_view(), name='_detail'),
#     path('<int:pk>/del', views.ExampleUpdateView.as_view(), name='_del'),
# ]
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('imageupload/', views.ImageUpload.as_view(), name='imageupload'),
    path('imagelistview/', views.ImageListView.as_view(), name='imagelistview'),
    path('simplelistview/', views.SimpleListView.as_view(), name='simplelistview'),
    path('itemupdateview/<int:pk>/', views.ItemUpdateView.as_view(), name='itemupdateview'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


htmx_urlpatterns = [
    path('search-item-author/', views.search_item_author, name='search-item-author'),
    path('search-item-title/', views.search_item_title, name='search-item-title'),
]

urlpatterns += htmx_urlpatterns
