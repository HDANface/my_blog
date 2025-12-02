from django.urls import path
from users import views


urlpatterns = [
    path('register/',views.UserCreateAPIView.as_view(),name='user_register'),
    path('login/',views.UserLoginAPIView.as_view(),name='user_login'),

]

