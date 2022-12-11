from functools import wraps
from typing import Callable

from pydolphinscheduler import configuration


def provide_user(func: Callable) -> Callable:
    """Decorator provides user from configuration when user is not provided.
    
    If you want to reuse a session or run the function as part of a
    database transaction, you pass it to the function, if not this wrapper
    will create one and close it for you.
    """
    session_args_idx = find_session_idx(func)

    @wraps(func)
    def wrapper(*args, **kwargs) -> Callable:
        if "user" in kwargs or session_args_idx < len(args):
            return func(*args, **kwargs)
        else:
            return func(*args, user=configuration.USER_NAME, **kwargs)

    return wrapper