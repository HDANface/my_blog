from django.urls import path

urlpatterns = [

]

# 媒体文件配置
from django.conf.urls.static import static
from django.conf import  settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
