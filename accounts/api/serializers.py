import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

User = get_user_model()
expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA


class UserRegistrationSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    token = serializers.SerializerMethodField(read_only=True)
    expires = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'token',
            'expires',
            'message',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_message(self,  obj):
        return "Thank you for your registering. Please verity your email before entering."

    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=-200)

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Password have to match.')
        return data

    def create(self, validated_data):
        print(validated_data)
        username = validated_data.get('username')
        email = validated_data.get('email')
        user_obj = User(username=username, email=email)
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        # user_obj.is_active = False
        return user_obj


class UserPublicSerializers(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'uri'
        ]

    def get_uri(self, obj):
        return api_reverse("user-status-list", kwargs={"username": obj.username}, request=self.context.get('request'))
        # return "/api/user/{id}/".format(id=obj.id)
