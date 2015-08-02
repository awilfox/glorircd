from collections import deque
from functools import wraps, partial
from types import MethodType


class ConditionError(Exception):
    pass


class PreconditionError(ConditionError):
    pass


class PostconditionError(ConditionError):
    pass


def _precondition(p_args, p_kwargs, is_meth, function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        # XXX hack
        if is_meth and isinstance(args[0], MethodType):
            c_args = args[1:]
        else:
            c_args = args[:]

        # Regular arguments
        for i, (arg, condition) in enumerate(zip(c_args, p_args)):
            if callable(condition):
                cond_val = condition(arg)
            else:
                cond_val = (arg == condition)

            if not cond_val:
                error = ("Precondition of {} failed: argument in "
                         "position {} bad").format(function.__name__,
                                                   i + 1)
                raise PreconditionError(error)

        # Keyword arguments
        for arg, value in kwargs.items():
            condition = p_kwargs[arg]
            if callable(condition):
                cond_val = condition(arg)
            else:
                cond_val = (arg == condition)

            if not cond_val:
                error = ("Precondition of {} failed: argument {} "
                         "bad").format(function.__name__, arg)
                raise PreconditionError(error)

        return function(*args, **kwargs)

    return wrapped


def precondition(*p_args, **p_kwargs):
    return partial(_precondition,  p_args, p_kwargs, False)


def preconditionmethod(*p_args, **p_kwargs):
    return partial(_precondition, p_args, p_kwargs, True)


def postcondition(condition):
    def wrapper(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            ret = function(*args, **kwargs)

            if callable(condition):
                cond_val = condition(ret)
            else:
                cond_val = (ret == condition)

            if not cond_val:
                error = ("Postcondition of {} failed: value {} "
                         "returned").format(function.__name, ret)
                raise PostconditionError(error)

            return ret

        return wrapped

    return wrapper


def postconditionmethod(condition):
    return postcondition(condition)


if __name__ == "__main__":
    @precondition(lambda x: x < 10 and x > 5, lambda y: y == 3)
    @postcondition(lambda x: x == None)
    def g(x, y):
        print(x, y)

    g(6, 3)
    g(6, 4)
