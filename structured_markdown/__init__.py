from .engine import *

def html(inp, name=None):
    """
    inp: SMD string to parse
    name: name of root div, if set to none, no root div will be returned
    returns: parsed html string
    """
    smd_instance = StructuredMarkdown(inp)
    return smd_instance.html(lines=None, name=name)

def css(inp):
    """
    inp: SMD string to parse
    returns: parsed css string
    """
    smd_instance = StructuredMarkdown(inp)
    return smd_instance.html(lines=None, selector=None)

def parse(inp, name=None):
    """
    inp: SMD string to parse
    name: name of root div, if set to none, no root div will be returned
    returns: tuple of parsed html string, parsed css string
    """
    # get kwargs for templating, maybe...
    # template name has to be a StructuredMarkdown object
    # and {{ name }} has to be a string, int, float, bool, etc.
    smd_instance = StructuredMarkdown(inp)
    return (
        smd_instance.html(lines=None, name=name),
        smd_instance.css(lines=None, selector=None),
    )

def parse_from_file(file_name, name=None):
    """
    file_name: path to file
    name: name of root div
    returns: tuple of parsed html string, parsed css string
    """
    with open(file_name, "r") as fin:
        inp = file.read()
    return parse(inp, name=Name)

def inline_style(inp, name=None):
    """
    inp: SMD string to parse
    name: name of root div
    returns: parsed html string with <style></style> block
    """
    smd_instance = StructuredMarkdown(inp)
    html = smd_instance.html(lines=None, name=name),
    css = smd_instance.css(lines=None, selector=None),

    return wrap_html(css, "style", smd_instance.ind_type) + html

def inline_style_from_file(file_name, name=None):
    """
    file_name: path to file
    name: name of root div
    returns: parsed html string with <style></style> block
    """
    with open(file_name, "r") as fin:
        inp = file.read()
    return inline_style(inp, name=name)
