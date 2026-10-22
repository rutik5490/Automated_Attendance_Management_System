from django.urls import path
from . import views

urlpatterns = [
    path('send-message/', views.send_custom_whatsapp_message, name='send_whatsapp_message'),
]