import setuptools

# quick instructions in case forgetten
# only reupload to pypi if new, fully completed features have been implemented and tested
# it's better to wait a few days, just for the BotD
# edit setup.py (this file) and bump the version number
# git add and git commit change to github, merge with master
# now, clear out build/* and dist/*
# cd to the project folder and type in terminal:
# $ python3 setup.py sdist bdist_wheel
# after that's done, type:
# $ twine upload dist/*
# after it's uploaded, install the new version:
# $ pip install --update structured-markdown

with open("README.md", "r") as fin:
    long_description = fin.read()

setuptools.setup(
    name="structured_markdown",
    version=0.1,
    description="Add an extra dimension to your markdown documents",
    long_description=long_description,
    url="https://github.com/Structured-Markdown/structured_markdown",
    author="Structured-Markdown",
    author_email="isaacimagine@gmail.com",
    license="MIT",
    packages=["structured_markdown"],
    zip_safe=False,
)
