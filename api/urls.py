from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.login),
    path('signout', views.logout),
    path('signup', views.register),
    path('user', views.content),
    path('folders', views.folders),
    path('resources', views.resources),
    path('folder', views.folder),
    path('folder/download', views.folder_download),
]