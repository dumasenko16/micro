import functools
from typing import Union

from passlib.context import CryptContext
import opentracing
from jaeger_client import Tracer
from opentracing_instrumentation.request_context import get_current_span, span_in_context

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


def verify_password(plain_password: Union[str, bytes], hashed_password: Union[str, bytes]) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: Union[str, bytes]):
    return pwd_context.hash(password)


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
