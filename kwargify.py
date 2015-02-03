# -*- coding: utf-8 -*-
import inspect

from functools32 import wraps


def kwargify(function):
    _method = hasattr(function, "im_func") or type(function).__name__ == "method"
    _defaults = {}
    argspec = inspect.getargspec(function)
    if _method:
        _args = argspec.args[1:]
    else:
        _args = argspec.args
    f_defaults = argspec.defaults
    if f_defaults is not None:
        for key, value in zip(_args[-len(f_defaults):], f_defaults):
            _defaults[key] = value

    @wraps(function)
    def wrapper(*args, **kwargs):
        pass_args = []
        if len(args) > len(_args):
            raise TypeError(
                "Too many parameters passed! ({} passed, {} possible)".format(
                    len(args), len(_args)))
        for arg in args:
            pass_args.append(arg)
        for arg in _args[len(args):]:
            if arg in kwargs:
                pass_args.append(kwargs[arg])
            elif arg in _defaults:
                pass_args.append(_defaults[arg])
            else:
                raise TypeError("Required parameter {} not found in the context!".format(arg))
        return function(*pass_args)
    return wrapper
