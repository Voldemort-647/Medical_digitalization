from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
# Create your views here.
def hello(request):
    return HttpResponse("hello this is my project")