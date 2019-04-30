from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class SimpleEchoView(TemplateView):

    template_name = "simpleEcho.html"

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)
