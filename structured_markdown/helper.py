from structured_markdown import *

# predefined
valid_ind = ["\t", "  ", "    "]
tokens = [
    ":",
    "=",
    "{{",
    "}}"
]
keywords = [
    "layer",
    "style",
]
mappings = {
    "layer": "div",
    "all": "*",
}

def wrap_html(to_wrap, tag, name=None):
    name = "" if name is None else " class={}".format(name)
    return "<{}{}>\n{}\n</{}>\n".format(
        tag, name,
        "\n".join("  " + line for line in to_wrap.split("\n")[:-1]),
        tag,
    )

def infer_ind(dirty):
    """
    self: StructuredMarkdown Object
    dirty: list of "dirty" lines
    returns: indentation type of the list self._valid_ind or ""
    """
    for line in dirty:
        leading = line.replace(line.lstrip(), "")
        if leading in valid_ind:
            return leading
        if leading != "" and leading != "\n" and leading not in valid_ind:
            raise IndentationError("Indentation type unsupported ({}).".format(repr(leading)))
    return ""

def tokenize(self, line):
    """
    self: StructuredMarkdown Object
    line: Line object to tokenize
    returns: tokenized line, list of strs
    """
    line = str(line)

    for token in tokens:
        line = line.replace(token, " {} ".format(token))

    return line.split()
