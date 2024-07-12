import logging, threading

local = threading.local()


def get_current_time(format=None):
    from datetime import datetime
    dt = datetime.now()
    if format:
        result = dt.strftime(format)
    else:
        result = dt.strftime("%Y/%m/%d %H:%M:%S")
    return result


def base_n(num, b):
    return ((num == 0) and "0") or \
        (base_n(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])


def generate_sid():
    sid = get_current_time("%H%M%S%f")
    sid = int(sid)
    sid = base_n(sid, 32)
    return "{}".format(sid)[::-1]


class RequestFilter(logging.Filter):
    def filter(self, record):
        request_id = getattr(local, 'request_id', None)
        if request_id is None:
            request_id = generate_sid()
        record.request_id = request_id
        local.request_id = request_id
        return True


handler = logging.StreamHandler()
handler.addFilter(RequestFilter())

log = logging.getLogger("")
log.setLevel(logging.DEBUG)
log.addHandler(handler)
