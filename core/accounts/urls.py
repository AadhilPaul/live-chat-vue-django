from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('testing/', views.testing),
    path('user/detail/', views.UserDetailView.as_view(), name='user-detail'),
    path('user/update/<int:pk>/', views.UserUpdateView.as_view(), name='user-update'),
    path('password_validator/', views.PasswordValidationApi.as_view(), name='password-validator')
]
