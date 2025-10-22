from django.contrib import admin
from django.urls import path, include
from wallet import views


app_name = 'wallet'
urlpatterns = [
    path('wallet/', views.wallet, name='wallet'),
    path('wallet/insert/', views.insert_money, name='insert_money'),
    path('wallet/withdraw/', views.withdraw_money, name='withdraw_money'),
    path('wallet/trade', views.trade, name='trade'),
]