import json
from functools import partial

from aiohttp import web


async def notify(recent_notifications, request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.HTTPBadRequest()

    recent_notifications.put_nowait(data)

    return web.HTTPOk()


def run_server(loop, recent_notifications):
    app = web.Application()
    app.add_routes([
        web.post('/notify', partial(notify, recent_notifications))
    ])
    web.run_app(app, loop=loop, port=8040)
