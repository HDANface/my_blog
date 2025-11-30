from django.urls import  path
from blog import views

urlpatterns = [
    path('articles/',views.ArticleViewSet.as_view(), name='blog'),
    path('articles/<int:pk>',views.ArticleView.as_view(), name='blog_pk'),

]