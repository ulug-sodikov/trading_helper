from django.urls import path

from . import views


app_name = 'auth_telegram'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login')
]
