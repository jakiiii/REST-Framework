from django.urls import path

from .views import UserDetailAPIView, UserStatusAPIView


urlpatterns = [
    path('<str:username>/', UserDetailAPIView.as_view(), name='detail'),
    path('<str:username>/status/', UserStatusAPIView.as_view(), name='status-list'),
]
