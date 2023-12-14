from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('resetpwd', views.resetpwd, name='resetpwd'),
    path('profile', views.profile, name='profile'),
    path('update', views.update_profile, name='update_profile'),
    path('delete', views.delete_profile, name='delete_profile'),
    path('logout', views.logout, name='logout'),
]
