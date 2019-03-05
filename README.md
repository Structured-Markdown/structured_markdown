# Structured-Markdown
I love markdown, but I've always wanted to use it to write more than just "flat" documents. 
Structured Markdown is an extension to markdown syntax that allows for nesting and (eventually) styling within one document.
So, how does it work?

## Overview
SMD is currently a python module that, when given a markdown file, will produce a formatted html string.
The general idea is that a static site could use these easy-to-write SMD files in place of html templates or the like.

## SMD vs MD
All squares are rectangles, but not all rectangles are squares.
The same can be said of SMD. 
With that out of the way, what's the difference?

A SMD document is made of layers.
Each layer has a name, and can contain markdown content and/or other layers. 

```
layer welcome:
  # Welcome to Structured-Markdown!
  this is markdown embedded within a layer.
```

This is a block of markdown within a layer whose name is `welcome`.
Because this is a parser, it returns html:

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

That's about it for now.
Not all features are implemented as this is still a WIP.
