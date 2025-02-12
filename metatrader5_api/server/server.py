import asyncio
from functools import partial

from aiohttp import web, WSMsgType

from create_terminal_connection import create_terminal_connection
from metatrader5_terminal_api.exceptions import MT5TerminalAPIException


# Symbols, ticks of which will be sent to ws client.
symbols_buffer = set()


async def symbol_exists(mt5_terminal, request):
    symbol = request.match_info['symbol'].upper()
    if mt5_terminal.symbol_exists(symbol):
        return web.Response()
    else:
        return web.HTTPNotFound()


async def get_symbols(request):
    return web.json_response({'symbols_buffer': list(symbols_buffer)})


async def add_symbol(mt5_terminal, request):
    symbol = request.match_info['symbol'].upper()

    if symbol not in symbols_buffer:
        # Add symbol to MarketWatch window. If symbol adding failed
        # (e.g. symbol doesn't exist) return HTTP 404.
        try:
            mt5_terminal.add_to_marketwatch(symbol)
        except MT5TerminalAPIException:
            return web.HTTPNotFound()

        symbols_buffer.add(symbol)

    return web.json_response({'symbols_buffer': list(symbols_buffer)})


async def discard_symbol(request):
    symbol = request.match_info['symbol'].upper()
    # TODO: remove symbol from MarketWatch window, otherwise
    #       too many symbols can slow down internet speed.
    symbols_buffer.discard(symbol)
    return web.json_response({'symbols_buffer': list(symbols_buffer)})


async def websocket_handler(mt5_terminal, request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    while True:
        for symbol in symbols_buffer:
            tick = mt5_terminal.get_last_tick(symbol)._asdict()
            await ws.send_json({
                'symbol': symbol,
                'time': tick['time'],
                'bid': tick['bid'],
                'ask': tick['ask']
            })

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
    mt5_terminal = create_terminal_connection()
    app = web.Application()
    app.add_routes([
        web.get('/symbol_exists/{symbol}', partial(symbol_exists, mt5_terminal)),
        web.get('/symbols_buffer', get_symbols),
        web.patch('/symbols_buffer/{symbol}', partial(add_symbol, mt5_terminal)),
        web.delete('/symbols_buffer/{symbol}', discard_symbol),
        web.get('/', partial(websocket_handler, mt5_terminal)),
    ])
    web.run_app(app)


if __name__ == "__main__":
    main()
