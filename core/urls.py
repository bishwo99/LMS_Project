from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category_list_create, name= 'category_list_create'),
]
