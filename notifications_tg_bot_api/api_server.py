import json
from functools import partial

from aiohttp import web


async def notify(queue, request):
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.HTTPBadRequest()

    queue.put_nowait(data)

    return web.HTTPOk()


def run_server(loop, queue):
    app = web.Application()
    app.add_routes([web.post('/notify', partial(notify, queue))])
    web.run_app(app, loop=loop, port=8040)
