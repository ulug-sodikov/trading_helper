from functools import partial

from aiogram import Dispatcher


async def stop_notifications(stopping_notifications, query):
    # stopping_notifications.add(query.data)
    await query.message.answer('fine!')


def _filter(query):
    return query.data.startswith('stop_alarm')


def create_dispatcher(stopping_notifications):
    dp = Dispatcher()
    dp.callback_query.register(
        partial(stop_notifications, stopping_notifications), _filter
    )

    return dp
