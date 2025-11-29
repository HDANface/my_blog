from django.urls import  path
from blog import views

urlpatterns = [
    path('articles/',views.ArticleViewSet.as_view(), name='blog'),
]