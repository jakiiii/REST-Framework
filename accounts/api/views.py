from django.db.models import Q
from django.contrib.auth import authenticate, get_user_model

from rest_framework import permissions,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .serializers import UserRegistrationSerializers
from .permissions import AnonPermissionOnly, IsOwnerOrReadOnly

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()


class AuthAPIView(APIView):
    permission_classes = [AnonPermissionOnly, IsOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail': 'You are already authenticated!'}, status=400)
        username = request.data.get('username')
        password = request.data.get('password')
        qs = User.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=username)
        ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                response = jwt_response_payload_handler(token, user, request=request)
                return Response(response)
        return Response({"details": "Invalid Credentials"}, status=401)


class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [AnonPermissionOnly]
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializers

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


# class RegisterAPIView(APIView):
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return Response({'detail': 'You are already register or authenticated!'}, status=400)
#
#         username = request.data.get('username')
#         email = request.data.get('email')
#         password = request.data.get('password')
#         password2 = request.data.get('password')
#
#         qs = User.objects.filter(
#             Q(username__iexact=username) | Q(email__iexact=username)
#         )
#         if password != password2:
#             Response({"details": "Password have to match."}, status=401)
#         if qs.exists():
#             return Response({"details": "This user already exists."}, status=401)
#         else:
#             user = User.objects.create(username=username, email=email)
#             user.set_password(password)
#             user.save()
#             # payload = jwt_payload_handler(user)
#             # token = jwt_encode_handler(payload)
#             # response = jwt_response_payload_handler(token, user, request=request)
#             # return Response(response, status=201)
#             return Response({"detail": "Thank for your registering. Please confirm your email."}, status=201)
#         return Response({"details": "Invalid Request"}, status=400)
