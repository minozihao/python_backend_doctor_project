import uvicorn
from fastapi import FastAPI

from src.router import init_router
from src.middleware import middleware_init


def start_app(*args_debug) -> FastAPI:
    """
    app entry point
    :param args_debug:
    :return: FastAPI app object
    """
    debug = False
    if args_debug and len(args_debug) > 0:
        debug = args_debug[0]
    app = FastAPI(title='doctor service',
                  version='0.1',
                  openapi_url='/doctor/openapi.json',
                  docs_url='/doctor/docs',
                  middleware=middleware_init(),
                  debug=debug)
    init_router(app)
    return app


if __name__ == '__main__':
    uvicorn.run(start_app(True), host="0.0.0.0", port=8081, workers=1, ws_max_size=2097152,
                limit_max_requests=500, timeout_keep_alive=5)
