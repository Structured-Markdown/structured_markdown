import structured_markdown as smd

path = "example.smd"

with open(path, "r") as fin:
    inp = fin.read()

print("----------\nsource file {}:\n\n{}".format(path, inp))
print("----------\nhtml extracted from {}:\n\n{}".format(path, smd.html(inp)))
print("----------\ncss extracted from {}:\n\n{}".format(path, smd.css(inp)))
print("----------\nhtml with style block extracted from {}:\n\n{}".format(path, smd.inline_style(inp)))
