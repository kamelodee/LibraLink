from django.views.generic import TemplateView

class SwaggerUIView(TemplateView):
    template_name = 'swagger-ui.html'