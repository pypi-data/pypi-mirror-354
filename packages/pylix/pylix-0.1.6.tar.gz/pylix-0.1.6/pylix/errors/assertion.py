from pylix.errors import ArgumentError, MathError, BaseError


def _edit_kwargs(wrong, kwargs: dict, exception) -> dict:
    if wrong in kwargs.values() or str(wrong) in kwargs.values():
        return kwargs
    if exception == ArgumentError:
        kwargs["wrong_argument"] = wrong
    elif exception == MathError:
        kwargs["wrong_argument"] = wrong
    elif exception == BaseError:
        kwargs["wrong"] = wrong
    return kwargs

def assert_type(var, type_, exception, **kwargs) -> None:
    if not isinstance(var, type_):
        raise exception(**_edit_kwargs(var, kwargs, exception))


def assert_range(var, start, end, exception, **kwargs) -> None:
    if var < start or var > end:
        raise exception(**_edit_kwargs(var, kwargs, exception))


def assert_below(var, max_, exception, **kwargs) -> None:
    if var >= max_:
        raise exception(**_edit_kwargs(var, kwargs, exception))


def assert_above(var, min_, exception, **kwargs) -> None:
    if var <= min_:
        raise exception(**_edit_kwargs(var, kwargs, exception))


def assert_equals(var, equaled, exception, **kwargs) -> None:
    if var != equaled:
        raise exception(**_edit_kwargs(var, kwargs, exception))

def assert_type_list(var, type_, exception, **kwargs) -> None:
    if any([not isinstance(i, type_) for i in var]):
        raise exception(**_edit_kwargs(var, kwargs, exception))

def assert_is_positiv(var, exception, **kwargs) -> None:
    if var < 0:
        raise exception(**_edit_kwargs(var, kwargs, exception))

def assert_is_negative(var, exception, **kwargs) -> None:
    if var > 0:
        raise exception(**_edit_kwargs(var, kwargs, exception))

def assert_not_zero(var, exception, **kwargs) -> None:
    if var == 0:
        raise exception(**_edit_kwargs(var, kwargs, exception))

def assert_types(var, types: tuple, exception, **kwargs) -> None:
    check: list = list()
    for type_ in types:
        check.append(isinstance(var, type_))
    if not any(check):
        raise exception(**_edit_kwargs(var, kwargs, exception))

def assert_is_none(var, exception, **kwargs) -> None:
    if var is not None:
        raise exception(**_edit_kwargs(var, kwargs, exception))

def assert_is_not_none(var, exception, **kwargs) -> None:
    if var is None:
        raise exception(**_edit_kwargs(var, kwargs, exception))

def assert_layer_list(var, assert_, arg: dict, exception, **kwargs) -> None:
    for element in var:
        assert_(element, **arg, exception=exception, **kwargs)

def assert_false(var: bool, exception, **kwargs) -> None:
    if var:
        raise exception(**_edit_kwargs(var, kwargs, exception))

def assert_true(var: bool, exception, **kwargs) -> None:
    if not var:
        raise exception(**_edit_kwargs(var, kwargs, exception))

def assert_types_list(var, types: tuple, exception, **kwargs) -> None:
    for element in var:
        assert_types(element, types, exception, **kwargs)
