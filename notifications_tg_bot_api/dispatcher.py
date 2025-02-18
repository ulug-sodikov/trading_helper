from functools import partial

from aiogram import Dispatcher


async def stop_alarm(queue, query):
    await query.message.answer('fine!')


def _filter(query):
    if query.data.startswith('stop_alarm'):
        return True
    else:
        return False


def create_dispatcher(queue):
    dp = Dispatcher()
    dp.callback_query.register(partial(echo, queue), _filter)

    return dp
