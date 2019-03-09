# Structured-Markdown
I love markdown, but I've always wanted to use it to write more than just "flat" documents.
Structured Markdown is an extension to markdown syntax that allows for nesting and styling within markdown documents.
So, how does it work?

## Overview
SMD is currently a python module that parses SMD into formatted html and css.
Currently, the module uses [mistune](https://github.com/lepture/mistune) to parse the markdown parts of .smd documents.
The general idea is that a static site could use these easy-to-write SMD files in place of html templates or the like.
If you're wondering what makes SMD so special, jump down to the [SMD vs MD](#smd-vs-md) section.

## Installation
Well, I finally got it working with pip, so

```
pip install structured-markdown
```

will now work!
(I'm using `Python >= 3.7`, btw.)

If you want to build from source, simply:

```
git clone https://github.com/Structured-Markdown/structured_markdown.git
cd structured_markdown
pip install .
```

(At least, that's what works for me.)

You may also need to install `mistune`, a markdown parser.

```
pip install mistune
```

Remember to use `pip3` if your working with Python 3.
I always forget to use `pip3`, so I thought you might like a little reminder 👍.

## Usage
To use SMD in your project, import it like so:

```python
import structured_markdown as smd
```

The main purpose of SMD is to parse .smd documents. This is pretty simple in `structured_markdown`:

```python
with open("example.smd", "r") as fin:
    inp = fin.read()

html, css = smd.parse(inp)
```

if you wish to get back only html or css, do the following:

```python
html = smd.parse(inp, html=True)
css = smd.parse(inp, css=True)
```

I'm planning to add templating capabilities to SMD, but it's not done yet 😔.

## SMD vs MD
All squares are rectangles, but not all rectangles are squares.
The same can be said of SMD - All Markdown documents are valid SMD documents, but not necessarily the other way around.
With that out of the way, what's the difference?

A SMD document is made of layers.
Each layer has a name, and can contain markdown content and/or other layers.

```
layer welcome:
  # Welcome to Structured-Markdown!
  this is markdown embedded within a layer.
```

This is a block of markdown within a layer whose name is `welcome`.
Here is the equivalent html.

```html
<div class='root'>
  <div class='welcome'>
    <h1>Welcome to Structured-Markdown!</h1>
    <p>this is markdown embedded within a layer.</p>
  </div>
</div>
```

Essentially, a layer is a `div`, the layer name being the `div`'s class.
Everything is put into a `root div` before the parsed SMD is returned.

Nesting is pretty simple:

```
layer welcome:
  # Welcome to Structured-Markdown!
  this is markdown embedded within a layer.
  layer nested:
    hey, this is nested
  more markdown after the nesting
```

Which becomes:

```html
<div class='root'>
  <div class='welcome'>
    <h1>Welcome to Structured-Markdown!</h1>
    <p>this is markdown embedded within a layer.</p>
    <div class='welcome'>
      <p>hey, this is nested</p>
    </div>
    <p>more markdown after the nesting</p>
  </div>
</div>
```

Where it really shines is when text is wrapped in complex formatting, like this navbar example:

```
layer navbar:
    layer logotype:
        # Templating Engine
    layer navlinks:
        1. [blog](/blog)
        2. [about](/about)
        3. [projects](/projects)
```

Note that the expanded html is longer and more verbose.

```html
<div class='root'>
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
</div>
```

So, what about styling?
I was feeling a bit lazy, and had to refactor a lot of code to introduce styling, so for now it's practically a one to one mapping to css.
Here's what styling looks like:

```
style layer:
    border = 1px solid
    font-family = sans-serif
```

use the `style` keyword to indent a style block - then, for each line in the style block, put the element on the left, followed by an equals sign, followed by the attribute.

```
style layer.navbar:
    background-color = #fff
```

All normal css selectors should work, note that you should use the word `layer` instead of `div`.
(You can still use div if you'd like, layer makes it look more readable.)

```
layer.navbar a:hover:
    color = #888
```

When parsed, SMD style blocks are fully transpiled into css. Hopefully, in the future I'll've implemented a better styling system, but this is what's here to stay for now.

That's about it for now.
Not all features are implemented as this is still a WIP.
