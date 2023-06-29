from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'app'
urlpatterns = [
    path("", views.index, name="homepage"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path('business_list/', business_list, name='business_list'),
    path('user_list/', user_list, name='user_list'),
    path('user_detail/<str:user_id>', views.user_detail, name='user_detail'),
    path('business_detail/<str:business_id>', views.business_detail, name='business_detail'),
    path('review_detail/<str:review_id>', views.review_detail, name='review_detail'),
    path('ver_diccionarios/', ver_diccionarios, name='ver_diccionarios'),
    path('resultado/', resultados, name='resultado'),





]