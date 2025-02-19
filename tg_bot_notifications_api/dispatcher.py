from functools import partial

from aiogram import Dispatcher


async def stop_notifications(running_notifications, query):
    key = query.data.removeprefix('stop:')
    running_notifications.discard(key)
    await query.answer('Notification stopped')


def _filter(query):
    return query.data.startswith('stop:')


def create_dispatcher(running_notifications):
    dp = Dispatcher()
    dp.callback_query.register(
        partial(stop_notifications, running_notifications), _filter
    )

    return dp
