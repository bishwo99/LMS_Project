from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.create_user_list, name= 'create_user_list'),
]
