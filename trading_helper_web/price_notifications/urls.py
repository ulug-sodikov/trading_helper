from django.urls import path

from . import views


app_name = 'price_notifications'
urlpatterns = [
    path('', views.index, name='index'),
]
