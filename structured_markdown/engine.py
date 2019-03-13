from . import *

import mistune
import copy

# this file is what I like to refer to as a "state module"
# it contains the classes nesessary to implement the interface
# but nothing more
# the goal is to keep this file as short as possible
# and do most of the interface implementation
# through "logic" (or "functional") modules.

class Line:
    __slots__ = ("line", "ind_type", "ind", "ind_level")

    def __init__(self, line, ind_type, ind=None):
        self.line = line
        self.ind = ind
        self.ind_type = ind_type

        if self.ind == None:
            self._cleanse()

    def __repr__(self):
        return "Line({}, {}, ind={})".format(
            repr(self.line),
            repr(self.ind_type),
            repr(self.ind),
        )

    def __str__(self): return self.line

    def __int__(self): return self.ind

    def _indentation(self): return self.line.replace(self.line.lstrip(), "")

    def _cleanse(self):
        leading = self._indentation()
        try:
            ind = len(leading) / len(self.ind_type)
        except ZeroDivisionError:
            ind = 0

        if int(ind) != ind and self.line != "\n" and self.line != "":
            raise IndentationError("Unexpected indentation type ({}).".format(repr(leading)))

        self.line = self.line.strip()
        self.ind = int(ind)

class StructuredMarkdown:
    def __init__(self, inp):
        """
        self: StructuredMarkdown Object
        inp: string to be processed
        returns: New StructuredMarkdown Object
        """
        # predefined
        self.valid_ind = ["\t", "  ", "    "]
        self.tokens = [
            ":",
            "=",
            "{{",
            "}}"
        ]
        self.keywords = [
            "layer",
            "style",
        ]
        self.mappings = {
            "layer": "div",
            "all": "*",
        }

        self.dirty = inp.split("\n") # each line in inp
        self.ind_type = self._infer_ind(self.dirty) # infer the indentation from first indent
        self.lines = [Line(line, self.ind_type) for line in self.dirty] # create a list of Line objects


    def _infer_ind(self, dirty):
        """
        dirty: list of "dirty" lines
        returns: indentation type of the list self._valid_ind or ""
        """
        for line in dirty:
            leading = line.replace(line.lstrip(), "")
            if leading in self.valid_ind:
                return leading
            if leading != "" and leading != "\n" and leading not in self.valid_ind:
                raise IndentationError("Indentation type unsupported ({}).".format(repr(leading)))
        return ""

    def _tokenize(self, line):
        """
        line: Line object to tokenize
        returns: tokenized line, list of strs
        """
        line = str(line)

        for token in self.tokens:
            line = line.replace(token, " {} ".format(token))

        return line.split()

    def render(self, **kwargs):
        # instead of looping through all items
        # maybe loop through each line and check for templates
        # then access the dictionary?
        # should be a lot more efficient
        lines = copy.deepcopy(self.lines)
        print(lines)
        for line in lines:
            for key, value in kwargs.items():
                template_tag = "{{{{ {} }}}}".format(key)
                print(template_tag)
                line.line = line.line.replace(template_tag, value)
                print(line)

        html = self.html(lines=lines)
        css = self.css(lines=lines)
        return html, css

    def html(self, lines=None, name=None):
        """
        self: StructuredMarkdown Object
        lines: list of Line Objects to parse, if set to None self.lines is used
        returns: html extracted from self
        """
        html = ""
        markdown = ""

        if lines is None:
            lines = copy.deepcopy(self.lines)

        while len(lines) > 0:
            line = lines.pop(0)
            tokenized = self._tokenize(line)

            if tokenized != [] and tokenized[0] in self.keywords and tokenized[-1] == ":":
                scope_name = tokenized[1:-1]

                if len(scope_name) > 1:
                    raise Exception("Name of a layer contains spaces ({}).".format(" ".join(scope_name)))

                scope_name = scope_name[0]

                scope = []
                while len(lines) > 0:
                    line = lines.pop(0)
                    if int(line) <= 0 and str(line) != "":
                        lines.insert(0, line)
                        break

                    line.ind -= 1
                    scope.append(line)

                if tokenized[0] == "layer":
                    html = html + mistune.markdown(markdown)
                    markdown = ""
                    html = html + self.html(scope, name=scope_name)
            else:
                markdown = markdown + self.ind_type * int(line) + str(line)

            markdown = markdown + "\n"

        html = html + mistune.markdown(markdown)

        if name == None:
            return html

        return wrap_html(html, "div", name=name)

    def css(self, lines=None, selector=None):
        """
        self: StructuredMarkdown Object
        lines: list of Line Objects to parse, if set to None self.lines is used
        returns: css extracted from self
        """
        css = ""

        if lines is None:
            lines = copy.deepcopy(self.lines)

        if selector is None:
            while len(lines) > 0:
                line = lines.pop(0)
                tokenized = self._tokenize(line)

                if tokenized != [] and tokenized[0] in self.keywords and tokenized[-1] == ":":
                    scope = []
                    while len(lines) > 0:
                        line = lines.pop(0)
                        if int(line) <= 0 and str(line) != "":
                            lines.insert(0, line)
                            break

                        line.ind -= 1
                        scope.append(line)

                    if tokenized[0] == "style":
                        scope_selector = " ".join(tokenized[1:-1])

                        for key, value in self.mappings.items():
                            scope_selector = scope_selector.replace(key, value)

                        css = css + self.css(scope, selector=scope_selector)
        else:
            css = "{} {{\n".format(selector)

            for line in lines:
                if str(line) != "":
                    attribute = list(map(lambda x: " ".join(x.split()), str(line).split("=")))
                    if len(attribute) != 2:
                        raise ValueError("extra or lack of equal sign in style assignment")

                    css = css + "  " + "{}: {};\n".format(*attribute)

            css = css + "}\n"

        return css

# TODO: add a "make_document" function that takes the body and produces a full document.

def wrap_html(to_wrap, tag, name=None):
    name = "" if name is None else " class={}".format(name)
    return "<{}{}>\n{}\n</{}>\n".format(
        tag, name,
        "\n".join("  " + line for line in to_wrap.split("\n")[:-1]),
        tag,
    )
