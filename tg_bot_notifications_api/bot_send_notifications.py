import asyncio

from utils import get_notification_key


async def bot_send_notifications(
        bot, recent_notifications, stopping_notifications
):
    while True:
        notification = await recent_notifications.get()
        asyncio.create_task(
            send_notifications_loop(bot, notification, stopping_notifications)
        )


async def send_notifications_loop(bot, notification, stopping_notifications):
    key = get_notification_key(notification)
    while key not in stopping_notifications:
        await bot.send_message(
            chat_id=notification['tg_user_id'],
            text=notification['text']
        )
        await asyncio.sleep(2)
