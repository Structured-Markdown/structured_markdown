import mistune

class Parser:
    def __init__(self, file):
        # stringify each line, and replace tabs with spaces
        self.file = file
        self.valid_ind = ["  ", "    "]
        self.ind = None
        self.ind_inds = list(":") # indentation indicators
        self.keywords = [
            "layer",
            "style"
        ]

        with open(self.file, "r") as fin:
            self.dirty_lines = [str(line).replace("\t", self.valid_ind[0]) for line in fin]

        # infer the indentation for parsing
        self.ind = self._infer_ind(self.dirty_lines)

        # clean up the lines
        self.lines = self._cleanse(self.dirty_lines)

        # tokenize and parse the file
        self.html = self._parse(self.lines)

    def __call__(self):
        return self.html

    def _indentation(self, line):
        return line.replace(line.lstrip(), "")

    def _infer_ind(self, dirty_lines):
        for line_number, line in enumerate(dirty_lines, 1):
            leading = self._indentation(line)
            if leading in self.valid_ind:
                return leading
            if leading != "" and leading not in self.valid_ind:
                raise IndentationError(
                    "Line {} in {}: '{}' indentation type unsupported.".format(line_number, self.file, leading)
                )
        return ""

    def _cleanse(self, dirty_lines):
        ind_levels = []
        cleansed = []

        for line_number, line in enumerate(dirty_lines, 1):
            leading = self._indentation(line)
            ind_level = len(leading) / len(self.ind)

            if int(ind_level) != ind_level and line != "\n" and line != "":
                raise IndentationError(
                    "Line {} in {}: '{}' unexpected indentation type.".format(line_number, self.file, leading)
                )

            ind_level = int(ind_level)
            line = line.strip()

            ind_levels.append(ind_level)
            cleansed.append(line)

        # make named tuple, maybe?
        return list(zip(ind_levels, cleansed))

    def _tokenize(self, line):
        for token in self.ind_inds:
            line = line.replace(token, " {} ".format(token))
        return " ".join(line.split()).split()

    def _styling(self, lines, selector):
        for indentation, line in lines:
            if indentation != 1:
                raise IndentationError("Variable indentation in styling block")
            try:
                element, value = list(map(lambda x: x.strip, line.split("=")))
            except:
                raise Exception("Incorrect styling assignment")

        # TODO: parse and return styling, implement branching logic in _parse

    def _parse(self, lines, name="root"):
        if isinstance(name, list):
            if len(name) != 1:
                raise Exception("Space in layer name")
            else:
                name = name[0]

        markdown = []
        html = ""
        css = ""

        while len(lines) > 0:
            line = lines.pop(0)
            tokenized = self._tokenize(line[1])

            if tokenized == []:
                markdown.append("")
            elif tokenized[0] in self.keywords and tokenized[-1] in self.ind_inds:
                # ideally define abstract behaviours in different functions, this should work for now
                scope_name = tokenized[1:-1]
                scope = []
                while len(lines) > 0:
                    if lines[0][0] == 0 and self._tokenize(lines[0][1]) != []:
                        break
                    line = lines.pop(0)
                    scope.append((line[0] - 1, line[1]))

                html = html + mistune.markdown("\n".join(markdown) + "\n")
                html = html + self._parse(lines=scope, name=scope_name)

                markdown = []
            else:
                markdown.append(line[1])

        html = html + mistune.markdown("\n".join(markdown) + "\n")

        return "<div class='{}'>\n".format(name) \
               + "\n".join(["  " + line for line in html.split("\n")[:-1]]) \
               + "\n</div>\n"

if __name__ == "__main__":
    print(Parser("example.smd")())
