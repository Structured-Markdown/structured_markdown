import mistune

def get_indentation(line):
    return len(line) - len(line.lstrip(' '))

def get_markdown(to_markdown):
    return mistune.markdown(to_markdown)

def parse(to_parse, div_class="root"):
    """
    to_parse: a list of strings
    returns: one html string
    """
    parsed = ""
    to_markdown = ""

    index = 0
    while index < len(to_parse):
        line = to_parse[index]
        indentation = get_indentation(line)
        line = line.strip()
        tokens = line.split()

        if line[-1] == ":":
            parsed = parsed + get_markdown(to_markdown)
            to_markdown = ""

            scope = []
            for future_index in range(len(to_parse[index + 1:])):
                future_line = to_parse[future_index]
                if get_indentation(future_line) <= indentation:
                    break
                scope.append(future_line)

            parsed = parsed + parse(scope, div_class=tokens[-1][:-1])

        else: to_markdown = to_markdown + to_parse[index].lstrip()

        index += 1

    if to_markdown != "": parsed = parsed + get_markdown(to_markdown)

    return "<div class={}>".format(div_class) + parsed + "</div>"

if __name__ == '__main__':
    file = "example.md"
    with open(file, "r") as fin:
        parsed = parse([str(line) for line in fin])
        print(parsed)
