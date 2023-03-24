
from django.contrib import admin
from django.urls import path, include

from main.views import *

urlpatterns = [
    path('', index, name="home"),
    path('category/<str:slug>/', category_detail, name='category'),
    path('recipe-detail/<int:pk>/', recipe_detail, name='detail'),
]
