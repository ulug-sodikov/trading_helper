import json
from functools import partial

from aiohttp import web


async def notify(new_notifications, request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.HTTPBadRequest()

    new_notifications.put_nowait(data)

    return web.HTTPOk()


def run_server(loop, new_notifications):
    app = web.Application()
    app.add_routes([
        web.post('/notify', partial(notify, new_notifications))
    ])
    web.run_app(app, loop=loop, port=8040)
