from utils.custom_exceptions import *


def get(args):
    if len(args) > 1:
        raise TooManyArgs
    elif not args[0].startswith('http'):
        raise NotAValidLink
    else:
        if args[0].startswith('"'):
            del args[0][0]
        if args[0].endswith('"'):
            del args[0][-1]
        return args[0].strip()
