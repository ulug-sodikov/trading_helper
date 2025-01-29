from django.http import HttpResponse
from django.template import loader


def index(request):
    return HttpResponse(loader.render_to_string('auth_telegram/index.html'))
