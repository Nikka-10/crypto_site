from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('', views.sign_up, name='sign_up'),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"),
]