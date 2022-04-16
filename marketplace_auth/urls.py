from django.urls import path
from marketplace_auth import views

urlpatterns = [
    path('registration/', views.user_registration),
    ]
