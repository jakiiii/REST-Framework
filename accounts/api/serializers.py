from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserRegistrationSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2'
        ]
        extra_kwargs = {'password': {'write_only': True}}

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
        return user_obj
