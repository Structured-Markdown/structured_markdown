from . import *

# these are helper functions
# they're used by classes and the like
# but the user shouldn't have to deal with them unless they really want to
# which is why they're not hidden

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

def infer_ind(dirty):
    """
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
    line: Line object to tokenize
    returns: tokenized line, list of strs
    """
    line = str(line)

    for token in tokens:
        line = line.replace(token, " {} ".format(token))

    return line.split()
