import hmac
from os import getenv
from hashlib import sha256

from dotenv import load_dotenv
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader


load_dotenv()


def index(request):
    template = loader.get_template('auth_telegram/index.html')
    context = {'tg_bot_username': getenv('TG_BOT_USERNAME')}

    return HttpResponse(template.render(context, request))


def login(request):
    tg_oauth_data = request.POST.dict()
    try:
        tg_oauth_data.pop('csrfmiddlewaretoken')
    except KeyError:
        return HttpResponseBadRequest()

    # Check authorization validity https://core.telegram.org/widgets/login#checking-authorization
    data_check_string = '\n'.join(
        f'{k}={v}' for k, v in sorted(tg_oauth_data.items())
        if k != 'hash'
    )
    tg_bot_token = getenv('TG_BOT_TOKEN')
    secret_key = sha256(tg_bot_token.encode()).digest()
    generated_hash = hmac.new(
        secret_key, data_check_string.encode(), sha256
    ).hexdigest()

    return HttpResponse(f'{generated_hash == tg_oauth_data.get("hash")}')
