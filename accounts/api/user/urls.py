from django.urls import path

from .views import UserDetailAPIView, UserStatusAPIView


urlpatterns = [
    path('<str:username>/', UserDetailAPIView.as_view(), name='api-user-detail'),
    path('<str:username>/status/', UserStatusAPIView.as_view(), name='user-status-list'),
]
