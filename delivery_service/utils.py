import uuid
import functools
from jaeger_client import Config, Tracer
import opentracing
from opentracing.scope_managers.contextvars import ContextVarsScopeManager
from opentracing_instrumentation.request_context import get_current_span, span_in_context
import logging

import schamas


def init_tracer(service: str = 'delivery_service'):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
        scope_manager=ContextVarsScopeManager()
    )
    return config.initialize_tracer()


def trace_it(tag, value):
    def inner(function):
        @functools.wraps(function)
        async def wrapper(*args, **kwargs):
            tracer = opentracing.global_tracer()
            with tracer.start_span(function.__name__, child_of=get_current_span()) as span:
                with span_in_context(span):
                    span.set_tag(tag, value)
                    return await function(*args, **kwargs)
        return wrapper
    return inner


def trace_it_sync(tag, value):
    def inner(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            tracer = opentracing.global_tracer()
            with tracer.start_span(function.__name__, child_of=get_current_span()) as span:
                with span_in_context(span):
                    span.set_tag(tag, value)
                    return function(*args, **kwargs)
        return wrapper
    return inner


deliveries = [
    schamas.Delivery(
        id=1,
        user_uuid=uuid.uuid4(),
        name=f'delivery 1'
    ),
    schamas.Delivery(
        id=2,
        user_uuid=uuid.uuid4(),
        name=f'delivery 2'
    ),
    schamas.Delivery(
        id=3,
        user_uuid=uuid.uuid4(),
        name=f'delivery 3'
    ),
]
