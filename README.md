# emmet.snippets

emmet.snippets provides an [UltiSnips](https://github.com/SirVer/ultisnips)
snippet that interprets [emmet's syntax](http://docs.emmet.io/abbreviations/syntax/)
for quickly generating HTML and XML tags and attributes.

# Features

* Live generation of tags and id and class attributes
* Fully supported syntax elements: `>`, `+`, `^`, `#`, `*`, `$`
* Proper indentation
* Dynamic jumps to tags without children and attributes without values
* First line of text is deleted automatically after the first jump
* Reasonable amount of tests implemented

# Usage

* Open a HTML or XML file in vim
* Type `e` on an empty line
* Press `<Tab>` to expand the snippet
* Start typing something that matches [emmet's
  syntax](http://docs.emmet.io/abbreviations/syntax/), e.g.
  `html>head>title^body>h1#title+p.myclass`

[![asciicast](https://asciinema.org/a/81977.png)](https://asciinema.org/a/81977)

# Installation

* Make sure [UltiSnips](https://github.com/SirVer/ultisnips) is installed
* Clone [emmet.snippets repository](https://github.com/jceb/emmet.snippets)
* Make sure it's present in your path variable
  * I recommend using [pathogen](https://github.com/tpope/vim-pathogen).  It's
    enough to clone the repository in `~/.vim/bundle`
* Test the functionality by opening a new buffer in vim `:vs`.  Change
  `filetype` to html `setf html`.  Write `et` and press `<Tab>` to expand the
  snippet and perform a self test
  * All tests should pass

# Configuration

Item numbering, `$`, can behave in two ways when combined with multiplication,
`*`.  Stacked multiplication combines all previous modifiers while non-stacked
multiplication just takes the tags direct multiplier into account.  The variable
`g:emmet_stacked_multiplication` controls the behavior.

To enable non-stacked multiplication execute `let
g:emmet_stacked_multiplication=0` (default).
```
# ul.list$*3>li.item$$*3
<ul class="list1">
    <li class="item01"></li>
    <li class="item02"></li>
    <li class="item03"></li>
</ul>
<ul class="list2">
    <li class="item01"></li>
    <li class="item02"></li>
    <li class="item03"></li>
</ul>
<ul class="list3">
    <li class="item01"></li>
    <li class="item02"></li>
    <li class="item03"></li>
</ul>
```

To enable stacked multiplication execute `let g:emmet_stacked_multiplication=1`.
```
# ul.list$*3>li.item$$*3
<ul class="list1">
    <li class="item01"></li>
    <li class="item02"></li>
    <li class="item03"></li>
</ul>
<ul class="list2">
    <li class="item04"></li>
    <li class="item05"></li>
    <li class="item06"></li>
</ul>
<ul class="list3">
    <li class="item07"></li>
    <li class="item08"></li>
    <li class="item09"></li>
</ul>
```

# Known Issues

* Not all syntax elements are supported yet.  The following are missing:
  * Grouping: `(..)`
  * Custom attributes: `[..]`
  * Changing numbering base and direction: `@-` and `@N`
  * Text: `{..}`
* Almost no error handling implemented
* Python 3 only
* No abbreviations implemented
* No support for CSS, SASS and other syntaxes

# Related Works

* [Emmet](http://emmet.io/) project - the essential toolkit for web-developers
* [emmet-vim](https://github.com/mattn/emmet-vim)
* [Sparkup](https://github.com/rstacruz/sparkup)
