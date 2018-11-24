import json

from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins

from status.models import Status
from status.api.serializers import StatusSerializer


def is_json(json_data):
    try:
        true_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid


class StatusListSearchAPIView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin, generics.ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = StatusSerializer
    passed_id = None

    def get_queryset(self):
        qs = Status.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) | Q(content__iexact=query)
            )
            return qs
        return qs

    def get_object(self):
        passed_id = self.request.GET.get('id', None) or self.passed_id
        queryset = self.get_queryset()
        obj = None
        if passed_id is not None:
            obj = get_object_or_404(queryset, id=passed_id)
            self.check_object_permissions(self.request, object)
        return obj

    def perform_destroy(self, instance):
        if instance is not None:
            return instance.delete()
        return None

    def get(self, request, *args, **kwargs):
        url_passed_id = self.request.GET.get('id', None)
        json_data = {}
        body_ = request.body
        if is_json(body_):
            json_data = json.loads(request.body)
        new_passed_id = json_data.get('id', None)
        passed_id = url_passed_id or new_passed_id or None
        self.passed_id = passed_id
        if passed_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        url_passed_id = self.request.GET.get('id', None)
        json_data = {}
        body_ = request.body
        if is_json(body_):
            json_data = json.loads(request.body)
        new_passed_id = json_data.get('id', None)

        requested_id = request.data.get('id')
        passed_id = url_passed_id or new_passed_id or requested_id or None
        self.passed_id = passed_id
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        url_passed_id = self.request.GET.get('id', None)
        json_data = {}
        body_ = request.body
        if is_json(body_):
            json_data = json.loads(request.body)
        new_passed_id = json_data.get('id', None)
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        url_passed_id = self.request.GET.get('id', None)
        json_data = {}
        body_ = request.body
        if is_json(body_):
            json_data = json.loads(request.body)
        new_passed_id = json_data.get('id', None)
        return self.destroy(request, *args, **kwargs)


# class StatusDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# class StatusUpdateAPIView(generics.UpdateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#
#
# class StatusDeleteAPIView(generics.DestroyAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
