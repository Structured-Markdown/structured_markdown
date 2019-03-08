from .engine import *

def parse(inp, html=None, css=None, name="root"):
    # get kwargs for templating, maybe...
    # template name has to be a StructuredMarkdown object
    # and {{ name }} has to be a string, int, float, bool, etc.

    if html is None and css is None: html, css = True, True
    elif html is None: html = False
    elif css is None: css = False

    smd_instance = StructuredMarkdown(inp)
    returned = []

    if html: returned.append(smd_instance.html(lines=None, name=name))
    if css: returned.append(smd_instance.css(lines=None, selector=None))

    return returned
