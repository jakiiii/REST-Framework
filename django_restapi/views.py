from django.views.generic import TemplateView


class DRFHomeTemplateView(TemplateView):
    template_name = 'base.html'
