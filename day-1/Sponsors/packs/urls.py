from django.urls import path
from . import views

urlpatterns = [
    path('', views.pack_list, name='pack_list'),
    path('subscribe/<int:pack_id>/', views.subscribe, name='subscribe'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('create-custom-plan/', views.create_custom_plan, name='create_custom_plan'),
    path('create-subscription/', views.create_subscription, name='create_subscription'),
]
