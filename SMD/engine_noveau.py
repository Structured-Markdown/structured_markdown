import mistune

class StructuredMarkdown:
    def __init__(self, fin, valid_ind, tokens, css_mapping):
        """
        self: StructuredMarkdown object
        fin: file input (file or file-like object)
        valid_ind: list of strings of indentation
        tokens: dict of tokens mapped to behaviour
        css_mapping: mapping of SMD names to css names
        returns: StructuredMarkdown object
        """
        self.dirty_lines = [str(line) for line in fin]

        self.valid_ind = ["  ", "    ", "\t"] if valid_ind is None else valid_ind

        self.tokens = {
            ":": "scope",
            "=": "assignment",
            ">": "css",
            ",": "css",
            ".": "css",
        } if tokens is None else tokens

        self.css_mapping = {
            "layer": "div",
            "all": "*",
        } if css_mapping is None else css_mapping

        self.keywords = {
            "layer": self._layer,
            "style": self._style,
        }

        self.SMD_datastructure = None

        self.ind = self.infer_ind(self.dirty_lines, valid_ind=self.valid_ind)
        self.lines = self.cleanse(self.dirty_lines, self.ind)

    def __call__(self.html=True, css=True):
        returned = self._layer(self.lines)
        if not html:
            returned.pop(0)
            if not css:
                return []
        if not css:
            returned.pop(1)
        return returned

    def _tokenize(self, line):
        for token in self.tokens.keys():
            line = line.replace(token, " {} ".format(token))
        return " ".join(line.split()).split()

    def _layer(lines, name="root"):
        # TODO: implement layering protocol

    def _style(lines, selector):
        """
        lines: list of tuples of indentation, line content
        selector: unparsed string of css selector
        """
        parsed_selector = []
        for token in self._tokenize(selector):
            parsed_selector.append(self.css_mapping.get(token, token))
        selector = "".join(parsed_selector)

        # TODO: parse lines, return them

    def _markdown(lines):
        # wrapper for mistune.markdown

    def _indentation(self, line):
        return line.replace(line.lstrip(), "")

    def infer_ind(self, dirty_lines, valid_ind):
        for line_number, line in enumerate(dirty_lines, 1):
            leading = self._indentation(line)
            if leading in valid_ind:
                return leading
            if leading != "" and leading not in valid_ind:
                raise Exception("'{}' Indentation type unsupported.").format(repr(leading))
        return ""

    def cleanse(self, dirty_lines, ind):
        ind_levels = []
        cleansed = []

        for line_number, line in enumerate(dirty_lines, 1):
            leading = self._indentation(line)
            ind_level = len(leading) / len(ind)

            if int(ind_level) != ind_level and line != "\n" and line != "":
                raise IndentationError(
                    "'{}' Unexpected indentation type.".format(repr(leading))
                )

            ind_level = int(ind_level)
            line = line.strip()

            ind_levels.append(ind_level)
            cleansed.append(line)

        # make named tuple, maybe?
        return list(zip(ind_levels, cleansed))
