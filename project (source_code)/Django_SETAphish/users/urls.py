from django.contrib import admin
from django.urls import path
from users import views

# Only allow register if makes sense in your environment.
# To do that, uncomment the line below 
# and the Register link in "login.html" template

urlpatterns = [
    #path('register', views.register, name='user_register'),
    path('login', views.login, name='user_login'),
    path('logout', views.logout, name='user_logout')
]
