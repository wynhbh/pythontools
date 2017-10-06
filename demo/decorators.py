import dis
import functools

def log(*new):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print 'begin call'
            if new:
                print '%s %s():' % (' '.join(new), func.__name__)
            func(*args, **kw)
            print 'end call'
        return wrapper
    return decorator

@log('we will call')
def now(d):
    print d, '1.1.1.1'

now('hello, ')
