from django.urls import path
from . import views

urlpatterns = [
  path('', views.AllRoomView.as_view(), name='rooms'),
  path('ifroom/', views.IfInRoom.as_view(), name='if-in-room'),
  path('room/create/', views.RoomCreateView.as_view(), name='room-create'),
  path('room/update/<str:code>/', views.RoomUpdateView.as_view(), name='room-update'),
  path('room/join/<str:code>/', views.RoomJoinView.as_view(), name='room-join'),
  path('room/leave/<str:code>/', views.RoomLeaveView.as_view(), name='room-leave'),
  path('room/detail/<str:code>/', views.RoomDetailView.as_view(), name='room-detail'),
  path('room/kick/<int:id>/<str:code>/', views.RoomKickUser.as_view(), name='room-kick-user')
]
