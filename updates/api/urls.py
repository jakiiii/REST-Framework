from django.urls import path, include

from .views import (
    UpdateModelDetailAPIView,
    UpdateModelListAPIView
)


urlpatterns = [
    path('', UpdateModelListAPIView.as_view()),
    path('<int:id>', UpdateModelDetailAPIView.as_view())
]
