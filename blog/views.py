from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class HomePageView(View):
    def get(self, request):
        return HttpResponse("Hello, world. You're at the polls page.")