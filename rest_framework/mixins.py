from django.http import JsonResponse


class JsonResponseMixin(object):
    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(self.get_content(context), **response_kwargs)

    def get_content(self, context):
        return context
