from django.urls import path
from . import views
from .views import convert_pdf_to_excel

urlpatterns = [
    path('api/login/', views.login, name='login'),
    path('create_user/', views.create_user, name='create_user'),
    path('api/convert_pdf_to_excel/', convert_pdf_to_excel),
]
