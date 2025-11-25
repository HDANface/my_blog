from django.urls import  path
from blog import views

urlpatterns = [
    path('',views.HomePageView.as_view(), name='blog'),
]