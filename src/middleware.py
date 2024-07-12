from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette_context.middleware.raw_middleware import RawContextMiddleware
from starlette_context import plugins


def middleware_init():
    return [
        # 1. CORS
        Middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'],
                   ),
        # 2. xid for tracing
        Middleware(
            RawContextMiddleware,
            plugins=(
                plugins.RequestIdPlugin(),
                plugins.CorrelationIdPlugin(),
            )
        )
    ]
