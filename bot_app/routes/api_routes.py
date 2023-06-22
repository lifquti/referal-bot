import os
import pathlib

from bot_app import config
from aiohttp import web

from bot_app.misc import routes, bot


@routes.post(f'/{config.ROUTE_URL}/payment')
async def get_handler(request):
    print(await request.json())
    try:
        print('ok')
    except Exception as e:
        return web.Response(status=404, body=str(e))
    return web.Response(status=200, body='ok')


@routes.get(f"/{config.ROUTE_URL}/log_errors")
async def get_errors(request):
    try:
        with open(os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), 'log_error.log'), 'r') as error_file:
            data = error_file.read()
        return web.Response(status=200, body=data)
    except Exception as e:
        return web.Response(status=404, body=str(e))


@routes.get(f"/{config.ROUTE_URL}/log_output")
async def get_errors(request):
    try:
        with open(os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), 'log_output.log'), 'r') as error_file:
            data = error_file.read()
        return web.Response(status=200, body=data)
    except Exception as e:
        return web.Response(status=404, body=str(e))
