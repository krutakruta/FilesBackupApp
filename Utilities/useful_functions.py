from functools import wraps


def check_type_decorator(*expected_types):
    def the_real_check_type_decorator(func):
        @wraps(func)
        def wrapper(self, obj):
            check_type(obj, *expected_types)
            func(self, obj)
        return wrapper
    return the_real_check_type_decorator


def check_type(obj, *expected_types):
    for expected_type in expected_types:
        if isinstance(obj, expected_type):
            return
    raise TypeError()