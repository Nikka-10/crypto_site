from django.contrib import admin
from django.urls import path, include
from wallet import views


app_name = 'wallet'
urlpatterns = [
    path('wallet/', views.wallet, name='wallet')
]