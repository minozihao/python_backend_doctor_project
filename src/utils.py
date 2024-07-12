from starlette_context import context


def get_request_context_correlation_id():
    return context.get('X-Correlation-ID') if context.exists() and context.__contains__(
        'X-Correlation-ID') else 'local-test-cid'


def get_request_context_request_id():
    return context.get('X-request-id') if context.exists() and context.__contains__(
        'X-request-id') else 'local-test-rid'
