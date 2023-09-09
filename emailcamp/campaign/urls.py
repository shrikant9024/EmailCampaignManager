from django.urls import path
from . import views

urlpatterns = [
    path('add_subscriber/', views.add_subscriber, name='add_subscriber'),
    path('subscribers_list/', views.subscribers_list, name='subscribers_list'),

    path('unsubscribe/<str:email>/', views.unsubscribe, name='unsubscribe'),


]
