import mistune

def tokenize(line, chars):
    for char in chars:
        line = line.replace(char, " {} ".format(char))
    return line.split()

def get_ind(line):
    return line.replace(line.lstrip(), "")

def remove_ind(line, ind_types, ind):
    return line[ind_types[ind]:]

def parse(lines, name="root"):
    # html and markdown blocks
    html = ""
    markdown = ""

    # dict of valid indentation types
    ind_types = {
        None: 0,
        "\t": 1,
        "  ": 2,
        "    ": 4,
    }

    # first thing is to determine the indentation type
    for line in lines:
        ind = line.replace(line.lstrip(), "")
        if ind in ind_types:
            break
        ind = None

    # list of indentation indicators and keywords
    ind_ind = [":"]
    keywords = ["layer"]

    while len(lines) > 0:
        # tokenize the zerost line, pop it from the queue
        line = lines.pop(0)
        tokens = tokenize(line, ind_ind)

        # make sure the line isn't blank
        if len(tokens) == 0:
            markdown = markdown + "\n"

        # check for keywords and indentation indicators
        elif tokens[0] in keywords and tokens[-1] in ind_ind:
            # get the name of the indented block
            scope_name = " ".join(tokens[1:-1])

            # parse and clear markdown block
            html = html + mistune.markdown(markdown)
            markdown = ""

            # go through the program and get the indented code scope
            scope = []
            for index, line in enumerate(lines):
                if get_ind(line) == "":
                    lines = lines[index:]
                    break
                scope.append(remove_ind(line, ind_types, ind))
            html = html + parse(scope, name=scope_name)

        # if it's not a formatting line, add it to the markdown block
        else:
            markdown = markdown + remove_ind(line, ind_types, ind)

    # add in any trailing markdown, clear the markdown block (a bit unnessary, tbh) and return
    if html == "":
        html = html + mistune.markdown(markdown)
    markdown = ""
    return "<div class='{}'>\n".format(name) \
           + "\n".join(["  " + line for line in html.split("\n")[:-1]]) \
           + "\n" + "</div>\n"

if __name__ == "__main__":
    file = "example.smd"
    with open(file, "r") as fin:
        parsed = parse([str(line) for line in fin])
    print(parsed)
