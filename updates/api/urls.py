from django.urls import path, include

from .views import (
    UpdateModelDetailAPIView,
    UpdateModelListAPIView
)


urlpatterns = [
    path('list', UpdateModelListAPIView.as_view()),
    path('detail/<int:id>', UpdateModelDetailAPIView.as_view())
]
