from django.contrib import admin
from django.urls import path
from django.conf.urls import  url
from api_server import settings 
from server import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r"dataset/datasets/",views.DatasetView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)