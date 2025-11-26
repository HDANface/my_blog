from django.urls import path
from users import views


urlpatterns = [
    path('register/',views.UserCreateAPIView.as_view(),name='user_register'),
    path('login/',views.UserLoginAPIView.as_view(),name='user_login'),

]

# 媒体文件配置
from django.conf.urls.static import static
from django.conf import  settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
