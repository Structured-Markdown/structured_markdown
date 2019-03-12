from . import *

# these are library functions
# this is how the user should mostly interact with the interface
# they should be short, easy to read, and efficient
# and also visible to the user

def template(func):
    """
    func: funtion that takes html and css arguments
    returns: new function that processes SMD string
    """
    def wrapper(inp, **kwargs):
        smd_instance = StructuredMarkdown(inp)
        html, css = smd_instance.render(**kwargs)
        return func(html, css)
    return wrapper

# TODO: replace docstrings with updated ones?

@template
def html(html, css):
    """
    inp: SMD string to parse
    returns: parsed html string
    """
    return html

@template
def css(html, css):
    """
    inp: SMD string to parse
    returns: parsed css string
    """
    return css

@template
def parse(html, css):
    """
    inp: SMD string to parse
    returns: tuple of parsed html string, parsed css string
    """
    return html, css

@template
def inline_style(html, css):
    """
    inp: SMD string to parse
    returns: parsed html string with <style></style> block
    """
    return wrap_html(css, "style") + html
