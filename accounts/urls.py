from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('change-password/', views.change_password, name='change_password'),
     path('signup/', views.signup_view, name='signup'),
]
