from functools import partial

from aiogram import Dispatcher


async def stop_alarm(queue, query):
    await query.message.answer('fine!')


def _filter(query):
    return query.data.startswith('stop_alarm')


def create_dispatcher(queue):
    dp = Dispatcher()
    dp.callback_query.register(partial(stop_alarm, queue), _filter)

    return dp
