from utils.custom_exceptions import *


def has_quotation_marks(li):
    for element in li:
        if element.startswith('"') and element.endswith('"'):
            return True


def has_semicolon(li):
    for element in li:
        if '; ' in element:
            return True


def get(args):
    out = list()
    if has_quotation_marks(args):
        for arg in args:
            arg = arg.replace('"', '')
            if len(arg) > 64:
                raise ShortTextTooLong
            else:
                out.append(arg)
    elif has_semicolon(args):
        args = " ".join(args)
        for arg in args:
            if len(arg) > 64:
                raise ShortTextTooLong
        out = args.split('; ')
    else:
        for arg in args:
            if len(arg) > 64:
                raise ShortTextTooLong
        out = args
    return out
