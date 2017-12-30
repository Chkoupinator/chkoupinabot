from utils.custom_exceptions import *


def get(args):
    if len(args) == 1 and '"' in args[0]:
        text = args[0].replace('"', '')
    elif len(args) > 0:
        text = ' '.join(args)

    if len(text) > 512:
        raise LongTextTooLong
    else:
        return text
