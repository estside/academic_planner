from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_view, name='chat_view'),
    path('chat/api/', views.chat_api, name='chat_api'),
]