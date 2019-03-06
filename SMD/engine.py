import mistune

class StructuredMarkdown:
    def __init__(self, fin, valid_ind=None, tokens=None, css_mapping=None):
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

        self.tokens = list(":=") if tokens is None else tokens

        self.css_mapping = {
            "layer": "div",
            "all": "*",
        } if css_mapping is None else css_mapping

        self.keywords = [
            "layer",
            "style",
        ]

        self.SMD_datastructure = None

        self.ind = self.infer_ind(self.dirty_lines, valid_ind=self.valid_ind)
        self.lines = self.cleanse(self.dirty_lines, self.ind)

    def __call__(self, html=True, css=True):
        returned = self._layer(self.lines)
        if not html:
            returned.pop(0)
            if not css:
                return []
        if not css:
            returned.pop(1)
        return returned

    def _tokenize(self, line):
        for token in self.tokens:
            line = line.replace(token, " {} ".format(token))
        return " ".join(line.split()).split()

    def _layer(self, lines, name="root"):
        markdown = []
        css = []
        html = []
        while len(lines) > 0:
            line = lines.pop(0)
            tokenized = self._tokenize(line[1])

            # markdown detection sandwitch
            if tokenized == []:
                markdown.append("")
            elif tokenized[0] in self.keywords and tokenized[-1] == ":":
                try: scope_name = tokenized[1:-1]
                except: raise("No name for scope")

                scope_name = scope_name[0]

                html.append(self._markdown(markdown))
                markdown = []

                scope = []
                while len(lines) > 0:
                    line = lines.pop(0)
                    if line[0] == 0 and self._tokenize(lines[0][1]) != []:
                        break
                    scope.append((line[0] - 1, line[1]))

                if tokenized[0] == "layer":
                    if len(scope_name) != 1:
                        raise Exception("Space in layer name")
                    html_string, css_string = self._layer(lines, name="scope_name")
                    html.append(html_string)
                    css.append(css_string)

                elif tokenized[0] == "style":
                    css.append(self._style(lines, scope_name))

            else:
                markdown.append(line[1])

        html.append(self._markdown(markdown))
        css_string = "\n".join(css) + "\n"
        html_string = "<div class='{}'>\n".format(name) \
                      + "\n".join("  " + line for line in html) \
                      + "\n</div>\n"

        return html_string, css_string

    def _style(self, lines, selector):
        """
        lines: list of tuples of indentation, line content
        selector: unparsed string of css selector
        """

        parsed_selector = []
        for token in self._tokenize(selector):
            parsed_selector.append(self.css_mapping.get(token, token))
        selector = "".join(parsed_selector)

        parsed_lines = []

        for indentation, line in lines:
            for token in self._tokenize(line):
                parsed_lines.append("{}: {};".format(*line.split("=")))
        lines = parsed_lines

        return selector + " \{\n" \
               + "\n".join("  " + line for line in lines) + "\n" \
               + "}\n"

    def _markdown(self, lines):
        # maybe make escape=True?
        return mistune.markdown("\n".join(line[1] for line in lines) + "\n", escape=False, hard_wrap=True)

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

if __name__ == "__main__":
    file = "example.smd"
    with open("example.smd", "r") as fin:
        example = StructuredMarkdown(fin)
    print(example(css=False))
