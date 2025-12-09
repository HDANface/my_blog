from django.urls import path
from comments import views

urlpatterns = [
    path('comments/',views.CommentsAPIView.as_view(),name='comments'),
]