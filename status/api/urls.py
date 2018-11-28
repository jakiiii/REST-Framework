from django.urls import path
from .views import (
    StatusListSearchAPIView,
    StatusAPIDetailView,
)


urlpatterns = [
    path('', StatusListSearchAPIView.as_view(), name='api-status-list'),
    path('<int:id>/', StatusAPIDetailView.as_view(), name="api-status-detail"),
]
