import datetime
import functools
from pathlib import Path


def logging(func):
    """
    Декоратор, логирующий работу кода.
    """
    p = Path('.')
    f_name = p.cwd() / 'decor.log'
    fh = open(f_name, 'w', encoding='UTF-8')

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        fh.write(f'call {wrapper.__name__!r} at {datetime.datetime.now()}\n')
        fh.write(f'with args {args}, kwargs {kwargs}')
        res = func(*args, **kwargs)
        fh.write(f'result {res}\n')
        return res
    return wrapper


@logging
def reverse_string(string, lower=None):
    s1 = ''.join(reversed(string))
    return s1.lower() if lower else s1

rs = reverse_string('QWERTYUIOP',)
rs = reverse_string('ASDFGHJKL', lower=True)
rs = reverse_string('ZXCVBNM')