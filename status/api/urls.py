from django.urls import path
from .views import (
    StatusListSearchAPIView,
    StatusAPIDetailView,
    # StatusDetailAPIView,
)


urlpatterns = [
    path('', StatusListSearchAPIView.as_view()),
    path('<int:id>/', StatusAPIDetailView.as_view(), name="api-status-detail"),
]
