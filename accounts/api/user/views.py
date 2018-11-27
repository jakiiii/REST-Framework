from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response

from .serializers import UserDetailSerializer, StatusInlineUserSerializer
from status.models import Status
from status.api.views import StatusListSearchAPIView

User = get_user_model()


class UserDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserDetailSerializer
    lookup_field = 'username'

    def get_serializer_context(self):
        return {'request': self.request}


class UserStatusAPIView(StatusListSearchAPIView):
    serializer_class = StatusInlineUserSerializer

    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get('username', None)
        if username is None:
            return Status.objects.none()
        return Status.objects.filter(user__username=username)

    def post(self, request, *args, **kwargs):
        return Response({'detail': 'Not allowed here.'}, status=400)


# class UserStatusAPIView(generics.ListAPIView):
#     serializer_class = StatusInlineUserSerializer
#
#     def get_queryset(self, *args, **kwargs):
#         username = self.kwargs.get('username', None)
#         if username is None:
#             return Status.objects.none()
#         return Status.objects.filter(user__username=username)
