import setuptools

with open("README.md", "r") as fin:
    long_description = fin.read()

setuptools.setup(
    name="structured_markdown",
    version=0.0,
    description="Add an extra dimension to your markdown documents",
    long_description=long_description,
    url="https://github.com/Structured-Markdown/structured_markdown",
    author="Structured-Markdown",
    author_email="isaacimagine@gmail.com",
    license="MIT",
    packages=["structured_markdown"],
    zip_safe=False,
)
