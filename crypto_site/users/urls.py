from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('', views.sign_up_page, name='sign_up'),
    path('login/', views.login_page, name="login"),
]