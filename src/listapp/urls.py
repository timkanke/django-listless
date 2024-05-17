from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views
from listapp.views import get_cat_list, add_cat, add_cat_submit, add_cat_cancel, delete_cat, edit_cat, edit_cat_submit
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
    path('crudtable/', views.CrudTable.as_view(), name='crudtable'),
    path('fancylist/', views.FancyList.as_view(), name='fancylist'),
    path('imageupload/', views.ImageUpload.as_view(), name='imageupload'),
    path('imagelistview/', views.ImageListView.as_view(), name='imagelistview'),
    path('simplelistview/', views.SimpleListView.as_view(), name='simplelistview'),
    path('itemupdateview/<int:pk>/', views.ItemUpdateView.as_view(), name='itemupdateview'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


htmx_urlpatterns = [
    path('search-item-author/', views.search_item_author, name='search-item-author'),
    path('search-item-title/', views.search_item_title, name='search-item-title'),
    path('get_cat_list/', get_cat_list, name='get_cat_list'),
    path('add_cat/', add_cat, name='add_cat'),
    path('add_cat_submit/', add_cat_submit, name='add_cat_submit'),
    path('add_cat_cancel/', add_cat_cancel, name='add_cat_cancel'),
    path('<int:cat_pk>/delete_cat/', delete_cat, name='delete_cat'),
    path('<int:cat_pk>/edit_cat/', edit_cat, name='edit_cat'),
    path('<int:cat_pk>/edit_cat_submit/', edit_cat_submit, name='edit_cat_submit'),
]

urlpatterns += htmx_urlpatterns
