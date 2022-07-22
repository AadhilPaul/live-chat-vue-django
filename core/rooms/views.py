from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def testing(request):
  return HttpResponse('<h1>Room testing.</h1>')
