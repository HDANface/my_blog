from django.urls import  path
from blog import views

urlpatterns = [
    path('articles/',views.ArticleViewSet.as_view(), name='blog'),
    path('articles/<int:pk>',views.ArticleView.as_view(), name='blog_pk'),
    path('tag/',views.TagView.as_view(), name='tag'),
    path('tag/<int:pk>',views.TagView.as_view(), name='tag_pk'),
    path('category/',views.CategoryView.as_view(), name='category'),
    path('category/<int:pk>',views.CategoryView.as_view(), name='category_pk'),
]

