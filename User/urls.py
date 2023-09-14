from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = 'home'),
    path("home/", views.home, name = 'home'),
    # path('login/', views.login_user, name='login'),
    # path('signup/', views.signup, name='signup'),
]