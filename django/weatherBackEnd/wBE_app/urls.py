from django.urls import path

from knox import views as knox_views

from . import views

urlpatterns = [
    path('daily', views.daily_API, name = 'daily'),
    path('hourly', views.hourly_API, name = 'hourly'),
    path('register', views.RegisterAPI.as_view(), name = 'register'),
    path('login', views.LoginAPI.as_view(), name = 'login'),
    path('logout', knox_views.LogoutView.as_view(), name = 'logout'),
    path('logoutall', knox_views.LogoutAllView.as_view(), name = 'logoutall'),
    path('user', views.UserAPI.as_view(), name = 'user'),
]
