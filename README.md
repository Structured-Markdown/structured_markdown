# Structured-Markdown
I love markdown, but I've always wanted to use it to write more than just "flat" documents.
Structured Markdown is an extension to markdown syntax that allows for nesting, styling, and templating within markdown documents.
So, how does it work?

## Table of Contents
Here are the different sections in this README.
If you're looking for the documentation, it's [here](https://structured-markdown.gitbook.io/python/).

* [Overview](#overview) - What's the difference between Structured Markdown and Vanilla Markdown? What's the point of this project?
* [Installation](#installation) - How to install and setup the `structured_markdown` Python package.
* [Usage](#usage) - Quick start guide on how to start using `structured_markdown` in your code.
* [SMD vs MD](#smd-vs-md) - A deeper explanation of the differences between SMD and MD

## Overview
Structured Markdown, or SMD, is a syntactic extension to Markdown.
SMD documents support structuring, styling, and templating.
`structured_markdown` is a Python module that parses SMD documents into formatted html and css.
Currently, the module uses [mistune](https://github.com/lepture/mistune) to parse the markdown parts of SMD documents.
this project aims to make SMD more commonplace in static site development.
If you're wondering what makes SMD different from normal MD, jump down to the [SMD vs MD](#smd-vs-md) section.

## Installation
To install the most recent stable version of `structured_markdown`, you can use `pip`.
This project was written using `Python >= 3.7`, but most earlier versions of Python 3 should work.

```
$ pip install structured-markdown
```

If you like the bleeding edge, you can build from source.

```
$ git clone https://github.com/Structured-Markdown/structured_markdown.git
$ cd structured_markdown
$ pip install .
```

You might also need to install `mistune`, a markdown parser, and m2r.

```
$ pip install mistune
$ pip install m2r
```

Remember to use `pip3` when working with Python 3.
(I always forget to use `pip3`, so I thought you might like a little reminder 👍.)

## Usage
To use `structured_markdown` in your projects, import it like so.
(We recommend using `smd` as an import alias as `structured_markdown` is a bit long.)

```python
import structured_markdown as smd
```

The main purpose of `structured_markdown` is to parse SMD documents. This is pretty simple:

```python
with open("example.smd", "r") as fin:
    inp = fin.read()

html, css = smd.parse(inp)
```
The `smd.parse` function takes a SMD string and returns formatted html and css
There are many other functions availiable in the `structured_markdown` package.

```python
html, css = smd.parse(inp)
html = smd.html(inp) # return only the html of a SMD document
css = smd.css(inp) # return only the css (styling) of a SMD document
full_html = smd.inline_style(inp) # return the html with an added style block
```

`structured_markdown` also supports basic templating.
We hope to extend `structured_markdown`'s templating features soon.

If you want to quickly template in some fields, you can add additional keywords to `structured_markdown` function calls.
For example, let's say you have the following SMD document called `template.smd`.

```
layer content:
    # {{ title }}
    SMD is pretty dang {{ adjective }}.
    {{ comment }}

style layer.content:
    font-family = {{ font_name }}
```

In this document, we have 3 templating fields: `title`, `adjective`, and `font_name`.
(Note that templating fields are wrapped in `{{}}`.
There needs to be a space around each templating field: `{{ this_is_valid }}`, `{{this_is_not}}`.)
To fill in these fields, we need to pass values to them.
Here's an example.

```python
import structured_markdown as smd

with open("example.smd", "r") as fin:
    inp = fin.read()

html, css = smd.parse(
    inp,
    title="Opinion on SMD",
    adjective="snazzy",
    comment="It's pretty neat"
    font_name="sans-serif"
)
```

You can even use pass markdown (and other SMD documents).

```python
html, css = smd.parse(
    inp,
    title="Opinion on SMD",
    adjective="*snazzy*", # markdown styling
    comment="layer comment:\n  It's pretty neat...", # SMD styling
    font_name="sans-serif"
)
```

That's a basic introduction to using SMD.
I hope you find it enjoyable 😁.

## SMD vs MD
This is a deeper dive into what SMD is and how it works.

A Structured Markdown can be thought of an extension of Markdown.
Just like how all squares are rectangles, but not all rectangles are squares, all Markdown documents are valid SMD documents, but not necessarily the other way around.
So, what are the extensions that SMD offers?

A SMD document is made of layers.
Each layer has a name and can contain markdown content and/or other layers.

```
layer welcome:
  # Welcome to Structured-Markdown!
  this is **Markdown** embedded within a layer.
```

This is a block of markdown within a layer whose name is `welcome`.
Here is the equivalent html.

```html
<div class='welcome'>
  <h1>Welcome to Structured-Markdown!</h1>
  <p>this is markdown embedded within a layer.</p>
</div>
```

Essentially, a layer is a `div`, the layer name being the `div`'s class.
Nesting is pretty simple:

```
layer welcome:
  # Welcome to Structured-Markdown!
  this is **Markdown** embedded within a layer.
  layer nested:
    Hey, this is nested.
  more Markdown after the nesting.
```

Which becomes:

```html
<div class='welcome'>
  <h1>Welcome to Structured-Markdown!</h1>
  <p>this is markdown embedded within a layer.</p>
  <div class='welcome'>
    <p>hey, this is nested</p>
  </div>
  <p>more markdown after the nesting</p>
</div>
```

Here is some simple SMD that expands to a lot more html:

```
layer navbar:
    layer logotype:
        # Templating Engine
    layer navlinks:
        1. [blog](/blog)
        2. [about](/about)
        3. [projects](/projects)
```

Here's the equivalent html.

```html
<div class='navbar'>
  <div class='logotype'>
    <h1>Templating Engine</h1>
  </div>
  <div class='navlinks'>
    <ol>
      <li><a href="/blog">blog</a></li>
      <li><a href="/about">about</a></li>
      <li><a href="/projects">projects</a></li>
    </ol>
  </div>
</div>
```

So, what about styling?
(Side Note: when I was implementing styling support, I had to refactor a large amount of code. because of this I didn't have time to implement a more advanced form of styling, so for now it's essentially a one to one mapping to css.)
Here's what styling looks like:

```
style layer:
    border = 1px solid
    font-family = sans-serif
```

Style blocks are created using the `style` keyword to indent a style block.
After the style block is a css selector.
For each line in the style block, put the css element on the left, followed by an equals sign, followed by the attribute.

```
style layer.navbar:
    background-color = #fff
```

All normal css selectors should work, note that you should use the word `layer` instead of `div`.
(You can still use `div` if you'd like, `layer` makes it look more readable and unified in my opinion.)
Here's another example fo a selector.

```
layer.navbar a:hover:
    color = #888
```

When parsed, SMD style blocks are fully transpiled into css. Hopefully, in the future I'll've implemented a better styling system, but this is what's here to stay for now.

[The section on templating is not completed yet...]

That's all for now. Thanks for following along this far.
