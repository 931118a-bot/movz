from django.contrib import admin
from django.urls import path, include
from movie import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('movie/', include('movie.urls')),
    path('common/', include('common.urls')),
    path('', views.index, name='index'),  # '/' 에 해당되는 path
]

# 이미지 URL 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)