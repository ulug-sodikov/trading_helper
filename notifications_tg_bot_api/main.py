import asyncio
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot

from dispatcher import create_dispatcher
from api_server import run_server


load_dotenv()


def main():
    loop = asyncio.new_event_loop()
    queue = asyncio.Queue()
    bot = Bot(token=getenv("TG_BOT_TOKEN"))
    dp = create_dispatcher(queue)
    loop.create_task(dp.start_polling(bot))
    run_server(loop, queue)


if __name__ == "__main__":
    main()
