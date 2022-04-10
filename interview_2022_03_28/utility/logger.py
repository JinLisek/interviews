import sys


def log_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
