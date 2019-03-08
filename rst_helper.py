import m2r

with open("README.rst", "w") as rst_file:
    rst_file.write(m2r.parse_from_file("README.md"))

print("Successfully updated README.rst")
