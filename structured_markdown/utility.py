from . import *

# utilitarian functions to be used by both the library and the user

# TODO: add a "make_document" function that takes the body and produces a full document.

def wrap_html(to_wrap, tag, name=None):
    name = "" if name is None else " class={}".format(name)
    return "<{}{}>\n{}\n</{}>\n".format(
        tag, name,
        "\n".join("  " + line for line in to_wrap.split("\n")[:-1]),
        tag,
    )
