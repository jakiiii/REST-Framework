from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse
from status.api.serializers import StatusInlineUserSerializer

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    # status_uri = serializers.SerializerMethodField(read_only=True)
    # recent_status = serializers.SerializerMethodField(read_only=True)
    # statuses        = serializers.HyperlinkedRelatedField(
    #                         source = 'status_set', # Status.objects.filter(user=user)
    #                         many=True,
    #                         read_only=True,
    #                         lookup_field ='id',
    #                         view_name='api-status:detail',
    #                     )
    # statuses = StatusInlineUserSerializer(source='status_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'uri',
            'status',
            # 'statuses',
            # 'status_uri',
            # 'recent_status'
        ]

    def get_uri(self, obj):
        return api_reverse("api-user-detail", kwargs={"username": obj.username}, request=self.context.get('request'))
        # return "/api/user/{id}/".format(id=obj.id)

    def get_status(self, obj):
        request = self.context.get('request')
        limit = 10
        if request:
            limit_query = request.GET.get('limit')
            try:
                limit = int(limit_query)
            except:
                pass
        qs = obj.status_set.all().order_by("-timestamp")  # [:10]
        data = {
            'uri': self.get_uri(obj) + "status/",
            'last': StatusInlineUserSerializer(qs.first()).data,
            'recent': StatusInlineUserSerializer(qs[:limit], many=True).data
        }
        return data

    # def get_status_uri(self, obj):
    #     return self.get_uri(obj) + "status/"

    # def get_recent_status(self, obj):
    #     qs = obj.status_set.all().order_by("-timestamp")[:10]
    #     return StatusInlineUserSerializer(qs[:10], many=True).data
