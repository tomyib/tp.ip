from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index_page, name='index-page'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', views.home, name='home'),
    path('buscar/', views.search, name='buscar'),
    path('registro/', views.registro, name='registro'),

    path('favourites/', views.getAllFavouritesByUser, name='favoritos'),
    path('favourites/add/', views.saveFavourite, name='agregar-favorito'),
    path('favourites/delete/', views.deleteFavourite, name='borrar-favorito'),

    path('exit/', LogoutView.as_view(), name='exit'),
]