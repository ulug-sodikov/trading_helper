import asyncio

from utils import get_notification_key, make_notification_inline_keyboard


async def bot_send_notifications(
        bot, new_notifications, running_notifications
):
    while True:
        notification = await new_notifications.get()
        asyncio.create_task(
            send_notifications_loop(bot, notification, running_notifications)
        )


async def send_notifications_loop(bot, notification, running_notifications):
    key = get_notification_key(notification)
    running_notifications.add(key)
    while key in running_notifications:
        await bot.send_message(
            chat_id=notification['tg_user_id'],
            text=notification['text'],
            reply_markup=make_notification_inline_keyboard(key)
        )
        await asyncio.sleep(1)
