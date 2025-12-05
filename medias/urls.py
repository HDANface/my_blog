from django.urls import path
from medias import views

urlpatterns = [
    path('ruda/<int:pk>', views.RUDAPI.as_view(), name='rudapi'),
    path('upload/', views.CreateMediaAPIView.as_view(), name='upload'),
]