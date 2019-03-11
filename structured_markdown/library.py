from structured_markdown import *

# def decorator_thingy(func):
#     def wrapper(inp, name=None, templates={}):
#         smd_instance = StructuredMarkdown(inp)

def html(inp):
    """
    inp: SMD string to parse
    name: name of root div, if set to none, no root div will be returned
    returns: parsed html string
    """
    smd_instance = StructuredMarkdown(inp)
    html, _ = smd_instance.render(inp)
    return html

def css(inp):
    """
    inp: SMD string to parse
    returns: parsed css string
    """
    smd_instance = StructuredMarkdown(inp)
    _, css = smd_instance.render(inp)
    return html

def parse(inp, name=None):
    """
    inp: SMD string to parse
    name: name of root div, if set to none, no root div will be returned
    returns: tuple of parsed html string, parsed css string
    """
    smd_instance = StructuredMarkdown(inp)
    return smd_instance.render(inp)

def inline_style(inp):
    """
    inp: SMD string to parse
    name: name of root div
    returns: parsed html string with <style></style> block
    """
    html, css = parse(inp)
    return wrap_html(css, "style") + html
