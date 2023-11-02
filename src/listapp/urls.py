from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views
# from .models import Item

app_name = "listapp"
# example_urlpatterns = [
#     path('', views.ExampleUpdateView.as_view(), name='_list'),
#     path('new/', views.ExampleUpdateView.as_view(), name='_create'),
#     path('<int:pk>/', views.ExampleUpdateView.as_view(), name='_detail'),
#     path('<int:pk>/del', views.ExampleUpdateView.as_view(), name='_del'),
# ]
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('simplelistview/', views.SimpleListView.as_view(), name='simplelistview'),
    path('itemupdateview/<int:pk>/', views.ItemUpdateView.as_view(), name='itemupdateview'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)