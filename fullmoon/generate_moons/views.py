from django.shortcuts import render
from django.http import HttpResponse as HTTP_res
# Create your views here.

def index(request):
	return HTTP_res("Hello World this is app")
