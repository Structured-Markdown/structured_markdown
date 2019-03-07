import structured_markdown as smd

path = "example.smd"

with open(path, "r") as fin:
    inp = fin.read()

html, css = smd.parse(inp)
print("----------\nsource file {}:\n\n{}".format(path, inp))
print("----------\nhtml extracted from {}:\n\n{}".format(path, html))
print("----------\ncss extracted from {}:\n\n{}".format(path, css))
