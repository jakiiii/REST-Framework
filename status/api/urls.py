from django.urls import path
from .views import (
    StatusListSearchAPIView,
    # StatusDetailAPIView,
)


urlpatterns = [
    path('', StatusListSearchAPIView.as_view()),
    # path('<int:pk>/', StatusDetailAPIView.as_view()),
]
