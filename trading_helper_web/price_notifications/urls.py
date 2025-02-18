from django.urls import path

from . import views


app_name = 'price_notifications'
urlpatterns = [
    path('', views.index, name='index'),
    path(
        'create_notification/',
        views.create_notification,
        name='create_notification'
    ),
    path(
        'delete_notification/<int:pk>/',
        views.delete_notification,
        name='delete_notification'
    )
]
