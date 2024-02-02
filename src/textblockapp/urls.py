from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views


app_name = 'textblockapp'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('diffview/<int:pk>/', views.DiffView.as_view(), name='diffview'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


htmx_urlpatterns = []

urlpatterns += htmx_urlpatterns
