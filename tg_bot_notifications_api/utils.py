from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def get_notification_key(notification):
    key_parts = []
    try:
        key_parts.append(notification['tg_user_id'])
        key_parts.append(notification['notification_id'])
        key_parts.append(notification['timestamp'])
    except KeyError:
        return None

    return '_'.join(map(str, key_parts))


def make_notification_inline_keyboard(key):
    button = InlineKeyboardButton(text='Stop', callback_data=f'stop:{key}')

    return InlineKeyboardMarkup(inline_keyboard=[[button]])
