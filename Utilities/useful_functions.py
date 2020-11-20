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


def parse_path_and_get_path_sheet(path):
    return split_path(path)[-1]


def split_path(path):
    return path.replace("\\", "/").split("/").filter(lambda item: item != "")


def split_path(path):
    return list(filter(lambda item: item != "",
                       path.replace("\\", "/").split("/")))

def process_req_and_remove_sub_proc_if_its_finished(
        str_request, processor, remove_processor):
    finished = processor.process_request(str_request)
    if finished:
        remove_processor()
    return finished
