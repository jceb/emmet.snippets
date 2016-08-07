# emmet.snippets

emmet.snippets provides an [UltiSnips](https://github.com/SirVer/ultisnips)
snippet that interprets [emmet's syntax](http://docs.emmet.io/abbreviations/syntax/)
for quickly generating HTML and XML tags and attributes.

# Features

* Live generation of elements and id and class attributes
* Fully supported syntax elements: `>`, `+`, `^`, `#`, `*`
* Proper indentation
* Reasonable amount of tests implemented

# Usage

* Open a HTML or XML file in vim
* Type `e` on an emty line
* Press `<Tab>` to expand the snippet
* Start typing something that matches [emmet's
  syntax](http://docs.emmet.io/abbreviations/syntax/), e.g.
  `html>head>title^body>h1#title+p.myclass`

[![asciicast](https://asciinema.org/a/81948.png)](https://asciinema.org/a/81948)

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

# Known Issues

* Not all syntax elements are supported yet.  The following are missing:
  * Grouping: `(..)`
  * Custom attributes: `[..]`
  * Item numbering: `$`
  * Changing numbering base and direction: `@-` and `@N`
  * Text: `{..}`
* Almost no error handling implemented
* First line containing the emmet string remains
* [Dynamic tab
  stops](https://github.com/SirVer/ultisnips/tree/master/doc/examples/tabstop-generation)
  are not implemented yet
* Python 3 only
* No abbreviations implemented
* No support for CSS, SASS and other syntaxes

# Related Works

* [Emmet](http://emmet.io/) project - the essential toolkit for web-developers
* [emmet-vim](https://github.com/mattn/emmet-vim)
* [Sparkup](https://github.com/rstacruz/sparkup)
