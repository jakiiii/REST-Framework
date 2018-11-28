from rest_framework import serializers
from status.models import Status
from rest_framework.reverse import reverse as api_reverse

from accounts.api.serializers import UserPublicSerializers


class StatusSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    user = UserPublicSerializers(read_only=True)

    class Meta:
        model = Status
        fields = [
            'uri',
            'id',
            'user',
            'content',
            'image'
        ]
        read_only_fields = ['user']

    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        content = data.get('content', None)
        if content is "":
            content = None
        image = data.get('image', None)
        if content is None and image is None:
            raise serializers.ValidationError('Content and Image field are required!')
        return super().clean(*args, **kwargs)

    def get_uri(self, obj):
        return api_reverse("api-status-detail", kwargs={"id": obj.id}, request=self.context.get('request'))
        # return "/api/status/{id}/".format(id=obj.id)


class StatusInlineUserSerializer(StatusSerializer):
    # uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Status
        fields = [
            'uri',
            'id',
            'content',
            'image'
        ]

    # def get_uri(self, obj):
        # return api_reverse("api-status-detail", kwargs={"id": obj.id}, request=self.context.get('request'))
        # return "/api/status/{id}/".format(id=obj.id)
