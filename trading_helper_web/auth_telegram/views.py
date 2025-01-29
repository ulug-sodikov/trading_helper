from os import getenv

from dotenv import load_dotenv
from django.http import HttpResponse
from django.template import loader


load_dotenv()


def index(request):
    template = loader.get_template('auth_telegram/index.html')
    context = {'tg_bot_username': getenv('TG_BOT_USERNAME')}

    return HttpResponse(template.render(context, request))
