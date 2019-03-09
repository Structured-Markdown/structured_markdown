import mistune
import copy

class Line:
    __slots__ = ("line", "ind_type", "ind", "ind_level")

    def __init__(self, line, ind_type, ind=None):
        self.line = line
        self.ind = ind
        self.ind_type = ind_type

        if self.ind == None:
            self._cleanse()

    def __repr__(self): return "Line({}, {}, ind={})".format(self.line, self.ind_type, self.ind)
    def __str__(self): return self.line
    def __int__(self): return self.ind

    def _indentation(self): return self.line.replace(self.line.lstrip(), "")

    def _cleanse(self):
        leading = self._indentation()
        ind = len(leading) / len(self.ind_type)

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
        self: StructuredMarkdown Object
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
        self: StructuredMarkdown Object
        line: Line object to tokenize
        returns: tokenized line, list of strs
        """
        line = str(line)

        for token in self.tokens:
            line = line.replace(token, " {} ".format(token))

        return line.split()

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

        return wrap_html(html, "div", self.ind_type, name=name)

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

                    css = css + self.ind_type + "{}: {};\n".format(*attribute)

            css = css + "}\n"

        return css

def wrap_html(to_wrap, tag, ind_type, name=None):
    name = "" if name is None else " class={}".format(name)
    return "<{}{}>\n{}\n</{}>\n".format(
        tag, name,
        "\n".join(ind_type + line for line in to_wrap.split("\n")[:-1]),
        tag,
    )
