from rest_framework import serializers
from status.models import Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = [
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
