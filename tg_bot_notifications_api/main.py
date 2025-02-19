import asyncio
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot

from dispatcher import create_dispatcher
from api_server import run_server
from bot_send_notifications import bot_send_notifications


load_dotenv()


def main():
    loop = asyncio.new_event_loop()
    new_notifications = asyncio.Queue()
    running_notifications = set()

    bot = Bot(token=getenv("TG_BOT_TOKEN"))
    dp = create_dispatcher(running_notifications)
    loop.create_task(dp.start_polling(bot))

    loop.create_task(bot_send_notifications(
        bot, new_notifications, running_notifications
    ))
    # run_server() called last, since it runs the event loop by calling
    # loop.run_until_complete(run_app()) under the hood
    run_server(loop, new_notifications)


if __name__ == "__main__":
    main()
