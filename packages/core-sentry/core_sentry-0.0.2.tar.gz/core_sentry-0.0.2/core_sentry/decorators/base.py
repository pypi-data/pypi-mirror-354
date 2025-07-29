# -*- coding: utf-8 -*-

import functools
import typing

import sentry_sdk


def init_sentry(
        _func: typing.Callable = None, *, dsn: str, env: str,
        tags: typing.Dict, **init_args):

    """
    It initializes the Sentry's SDK and optionally integrations...

    :param _func:
    :param dsn: The DSN tells the SDK where to send the events.
    :param env: Environments tell you where an error occurred (production, staging).

    :param tags:
        Tags are key/value string pairs that are both indexed and searchable. Tags power
        features in sentry.io such as filters and tag-distribution maps. Tags also help you quickly
        both access related events and view the tag distribution for a set of events.
        More Info: https://docs.sentry.io/platforms/python/enriching-events/tags/

    For other parameters: https://docs.sentry.io/platforms/python/configuration/options/
    """

    def decorator(func: typing.Callable) -> typing.Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            sentry_sdk.init(dsn=dsn, environment=env, traces_sample_rate=1.0, **init_args)

            for tag, value in tags.items():
                sentry_sdk.set_tag(key=tag, value=value)

            return func(*args, **kwargs)

        return wrapper

    return decorator(_func) if _func else decorator
