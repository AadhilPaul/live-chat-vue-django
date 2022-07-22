from django.urls import path, include
from . import views

urlpatterns = [
    path('testing/', views.testing),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
