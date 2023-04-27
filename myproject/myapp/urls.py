from django.urls import path
from .views import MyTokenObtainPairView, get_nickname

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/nickname/', get_nickname, name='get_nickname'),
]
