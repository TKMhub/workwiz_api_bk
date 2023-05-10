from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.login, name='login'),
    path('upload/', views.upload_pdf, name='upload_pdf'),
]
