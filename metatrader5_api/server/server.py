import asyncio

from aiohttp import web, WSMsgType


# Symbols, ticks of which will be sent to ws client.
symbols_buffer = set()


async def get_symbols(request):
    return web.json_response({'symbols_buffer': list(symbols_buffer)})


async def add_symbol(request):
    symbol = request.match_info['symbol']
    # TODO: check if symbol is valid before adding it to symbols buffer.
    symbols_buffer.add(symbol)
    return web.json_response({'symbols_buffer': list(symbols_buffer)})


async def discard_symbol(request):
    symbol = request.match_info['symbol']
    symbols_buffer.discard(symbol)
    return web.json_response({'symbols_buffer': list(symbols_buffer)})


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    while True:
        for symbol in symbols_buffer:
            await ws.send_json({'symbol': symbol})

        try:
            # Performs the role of asyncio.sleep, too.
            msg = await ws.receive(timeout=0.5)
        except asyncio.TimeoutError:
            pass
        else:
            if msg.type == WSMsgType.CLOSE:
                await ws.close()
                break

    return ws


def main():
    app = web.Application()
    app.add_routes([
        web.get('/symbols_buffer', get_symbols),
        web.patch('/symbols_buffer/{symbol}', add_symbol),
        web.delete('/symbols_buffer/{symbol}', discard_symbol),
        web.get('/', websocket_handler),
    ])
    web.run_app(app)


if __name__ == "__main__":
    main()
