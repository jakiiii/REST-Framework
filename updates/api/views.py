import json
from django.http import HttpResponse
from django.views.generic import View

from updates.forms import UpdateModelFrom
from updates.models import Update as UpdateModel

from rest_framework.mixins import HttpResponseMixin
from .mixins import CSRFExemptMixin


class UpdateModelDetailAPIView(HttpResponseMixin, CSRFExemptMixin, View):
    is_json = True

    def get(self, request, id, *args, **kwargs):
        obj = UpdateModel.objects.get(id=id)
        json_data = obj.serialize()
        return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        json_data = json.dumps({'message': 'Not allowed! Please api/updates/ create endpoint.'})
        return self.render_to_response(json_data, status=405)

    def put(self, request, *args, **kwargs):
        json_data = {}
        return self.render_to_response(json_data)

    def delete(self, request, *args, **kwargs):
        json_data = {}
        return self.render_to_response(json_data)


class UpdateModelListAPIView(HttpResponseMixin, CSRFExemptMixin, View):
    is_json = True

    def get(self, request, *args, **kwargs):
        qs = UpdateModel.objects.all()
        json_data = qs.serialize()
        return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        form = UpdateModelFrom(request.POST)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = obj.serialize()
            return self.render_to_response(obj_data, status=201)
        if form.errors():
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)
        data = json.dumps({'message': 'Unknown Data'})
        return self.render_to_response(data, status=400)

    def delete(self, request, *args, **kwargs):
        data = json.dumps({'message': 'You can not delete entire list!'})
        return self.render_to_response(data, status=403)
