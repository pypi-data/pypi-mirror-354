from functools import wraps
from inspect import iscoroutinefunction
from time import time

from kalib import Who, json


def attach(name, method):
    def wrapper(func):
        setattr(func, name, method.fget)
        return func
    return wrapper


def log_long_wait(func):

    def get_threshold(node):
        config = getattr(node, 'settings', node.config)
        return getattr(config, 'logging_threshold', 1.0)

    if iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(node, *args, **kw):
            start = time()
            result = await func(node, *args, **kw)
            spent = time() - start


            if spent >= get_threshold(node):
                args, kw = json.repr((node, *args)), json.repr(kw)
                msg = f'long {spent:0.2f}s call {Who(func)}(*{args=}, **{kw=})'
                node.log.warning(msg, stack=1)

            return result

    else:
        @wraps(func)
        def wrapper(node, *args, **kw):
            start = time()
            result = func(node, *args, **kw)

            spent = time() - start
            if spent >= get_threshold(node):
                args, kw = json.repr((node, *args)), json.repr(kw)
                msg = f'long {spent:0.2f}s call {Who(func)}(*{args=}, **{kw=})'
                node.log.warning(msg, stack=1)

            return result

    return wrapper
