from SMD import engine

example_file = "example.smd"

with open(example_file, "r") as fin:
    inp = fin.read()

example = engine.StructuredMarkdown(inp)
print(example.css())
