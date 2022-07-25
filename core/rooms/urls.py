from django.urls import path
from . import views

urlpatterns = [
  path('', views.testing),
  path('room/create/', views.RoomCreateView.as_view(), name='room-create')
]