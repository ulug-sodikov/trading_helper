from os import getenv

from dotenv import load_dotenv
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.contrib.auth import authenticate, login


load_dotenv()


def index(request):
    template = loader.get_template('auth_telegram/index.html')
    context = {'tg_bot_username': getenv('TG_BOT_USERNAME')}

    return HttpResponse(template.render(context, request))


def login_user(request):
    tg_oauth_data = request.POST.dict()
    try:
        tg_oauth_data.pop('csrfmiddlewaretoken')
    except KeyError:
        return HttpResponseBadRequest()

    user = authenticate(tg_oauth_data)
    if user is not None:
        login(request, user)

    return HttpResponse(f'username: {user.username}')
