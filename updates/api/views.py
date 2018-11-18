import json
from django.http import HttpResponse
from django.views.generic import View

from updates.forms import UpdateModelFrom
from updates.models import Update as UpdateModel

from rest_framework.mixins import HttpResponseMixin
from .mixins import CSRFExemptMixin

from .utils import is_json


class UpdateModelDetailAPIView(HttpResponseMixin, CSRFExemptMixin, View):
    is_json = True

    def get_object(self, id=None):
        qs = UpdateModel.objects.filter(id=id)
        if qs.count() == 1:
            return qs.filter()
        return None

    def get(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({"message": "Update Not Found."})
            return self.render_to_response(error_data, status=404)
        json_data = obj.serialize()
        return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        json_data = json.dumps({'message': 'Not allowed! Please api/updates/ create endpoint.'})
        return self.render_to_response(json_data, status=405)

    def put(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({"message": "Update Not Found."})
            return self.render_to_response(error_data, status=404)
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({"message": "Invalid data. Please send data with json format."})
            return self.render_to_response(error_data, status=400)
        new_data = json.loads(request.body)
        print(new_data)
        json_data = json.dumps({"message": "some random message"})
        return self.render_to_response(json_data)

    def delete(self, request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({"message": "Update Not Found."})
            return self.render_to_response(error_data, status=404)
        json_data = json.dumps({"message": "some random message"})
        return self.render_to_response(json_data)


class UpdateModelListAPIView(HttpResponseMixin, CSRFExemptMixin, View):
    is_json = True

    def get(self, request, *args, **kwargs):
        qs = UpdateModel.objects.all()
        json_data = qs.serialize()
        return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({"message": "Invalid data. Please send data with json format."})
            return self.render_to_response(error_data, status=400)

        data = json.loads(request.body)
        form = UpdateModelFrom(data)
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
