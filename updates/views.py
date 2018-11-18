import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.core.serializers import serialize

from .models import Update
from rest_framework.mixins import JsonResponseMixin


# Create your views here.
def json_example_view(request):
    data = {
        'count': 100000,
        'content': 'some random content'
    }
    json_data = json.dumps(data)
    # return JsonResponse(data)
    return HttpResponse(json_data)


class JsonCBV(View):
    def get(self, request, *args, **kwargs):
        data = {
            'count': 100000,
            'content': 'some random content'
        }
        return JsonResponse(data)


class JsonCBV2(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            'count': 100000,
            'content': 'some random content'
        }
        return self.render_to_json_response(data)


class SerializedListView(View):
    def get(self, request, *args, **kwargs):
        qs = Update.objects.all()
        json_data = qs.serialize()
        return HttpResponse(json_data, content_type='application/json')


class SerializedDetailView(View):
    def get(self, request, *args, **kwargs):
        obj = Update.objects.get(id=1)
        json_data = obj.serialize()
        return HttpResponse(json_data, content_type='application/json')
