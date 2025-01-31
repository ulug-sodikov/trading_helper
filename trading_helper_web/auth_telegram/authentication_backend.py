import hmac
from os import getenv
from hashlib import sha256

from dotenv import load_dotenv
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


load_dotenv()


# https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#writing-an-authentication-backend
class TelegramAuthenticationBackend(BaseBackend):
    """
    Authenticate against Telegram oauth data.
    """
    def authenticate(self, tg_oauth_data):
        # Check authorization validity (https://core.telegram.org/widgets/login#checking-authorization)
        data_check_string = '\n'.join(
            f'{k}={v}' for k, v in sorted(tg_oauth_data.items())
            if k != 'hash'
        )
        tg_bot_token = getenv('TG_BOT_TOKEN')
        secret_key = sha256(tg_bot_token.encode()).digest()
        generated_hash = hmac.new(
            secret_key, data_check_string.encode(), sha256
        ).hexdigest()

        if generated_hash == tg_oauth_data['hash']:
            return self.get_or_create_user(str(tg_oauth_data['id']))
        else:
            return None

    def get_or_create_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return User.objects.create_user(username=username)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
