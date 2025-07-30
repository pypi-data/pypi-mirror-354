import functools
import warnings

if hasattr(functools, "deprecated"):
    deprecated = functools.deprecated  # Use built-in in Python 3.13+
else:
    def deprecated(arg=None):
        """Fallback for @deprecated and @deprecated("reason") in Python < 3.13."""

        if callable(arg):  # used as @deprecated without reason
            func = arg
            msg = f"'{func.__name__}' is deprecated."

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
                return func(*args, **kwargs)

            return wrapper

        reason = arg  # used as @deprecated("reason")

        def decorator(func):
            msg = f"'{func.__name__}' is deprecated."
            if reason:
                msg += f" Reason: {reason}"

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
                return func(*args, **kwargs)

            return wrapper

        return decorator


def TODO(arg=None):
    """
    This decorator gives a warning if a not fully implemented function is called, but still executes it.

    Ce Décorateur avertit, si une fonction qui n'a pas encore été implémentée en entier est demandée, mais elle
    s'exécute quand même.

    :param arg: The function (Python does that by default) if used as @TODO else it is the wanted message.
    :return:
    """
    if callable(arg):  # used as @TODO
        @functools.wraps(arg)
        def wrapper(*args, **kwargs):
            warnings.warn(f"{arg.__name__} - TODO: implementation pending.", stacklevel=2)
            return arg(*args, **kwargs)
        return wrapper

    def decorator(func):  # Used as @TODO("custom message")
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            message = arg or "implementation pending"
            warnings.warn(f"{func.__name__} - TODO: {message}.", stacklevel=2)
            return func(*args, **kwargs)
        return wrapper

    return decorator

def to_test(arg=None):
    """
    This decorator gives a warning if the testing for the function has not yet been implemented.
    The function still executes.

    Ce décorateur émet un avertissement si le test de la fonction n'a pas encore été mis en œuvre.
    La fonction s'exécute quand même.

    :param arg: The function (Python does that by default> if used as @to_test else it is the wanted message.
    :return:
    """
    if callable(arg):  # used as @to_test
        @functools.wraps(arg)
        def wrapper(*args, **kwargs):
            warnings.warn(f"{arg.__name__} - to_test: testing pending.", stacklevel=2)
            return arg(*args, **kwargs)
        return wrapper

    def decorator(func):  # Used as @to_test("custom message")
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            message = arg or "testing pending"
            warnings.warn(f"{func.__name__} - to_test: {message}.", stacklevel=2)
            return func(*args, **kwargs)
        return wrapper

    return decorator
