from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"),
    path('verify-2fa', views.verify_2fa, name='verify_2fa'),
    path('toggle_2fa', views.toggle_2fa, name='toggle_2fa'),
]